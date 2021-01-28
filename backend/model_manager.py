import datetime as dt
import re
from typing import Tuple, Dict, List

import tensorflow as tf
from fastapi import UploadFile

from api.model import ModelMetadata, TrainingRequest
from logger import backend_logger
from .db.redis_handler import RedisHandler
from .data_handler import DataHandler
from .dataset_manager import DatasetManager
from .exceptions import ErroneousModelException, ModelNotAvailableException, NoDataForCodebookException, \
    InvalidModelIdException


class ModelManager(object):
    _singleton = None

    def __new__(cls, *args, **kwargs):
        if cls._singleton is None:
            backend_logger.info('Instantiating ModelManager!')
            cls._singleton = super(ModelManager, cls).__new__(cls)
        return cls._singleton

    @staticmethod
    def is_available(cb_name: str, model_version: str = "default", complete_check: bool = False) -> bool:
        """
        Checks if the model for the given codebook is available
        :param cb_name: the codebook name
        :param model_version: version tag of the model (e.g. "default")
        :param complete_check: if true, not only the Redis cache but also the physical directory gets checked
               for the existence of the model
        :return: True if the model for the codebook is available and False otherwise
        """
        try:
            if not complete_check:
                return RedisHandler().get_model_metadata(cb_name=cb_name, model_version=model_version) is not None
            else:
                model_dir = DataHandler.get_model_directory(cb_name, model_version=model_version)
                return tf.saved_model.contains_saved_model(model_dir)
        except (ModelNotAvailableException, NoDataForCodebookException):
            return False

    @staticmethod
    def load(cb_name: str, model_version: str = "default"):
        """
        Loads the Tensorflow Estimator model for the given Codebook
        :param cb_name: the codebook name
        :param model_version: version tag of the model (e.g. "default")
        :return: the Tensorflow Estimator model for the given Codebook
        """
        model_dir = DataHandler.get_model_directory(cb_name, model_version=model_version)
        estimator = tf.saved_model.load(str(model_dir))
        if estimator.signatures["predict"] is None:
            raise ErroneousModelException(
                msg=f"Estimator / Model of version '{model_version}' for Codebook %s is erroneous!" % cb_name)

        return estimator

    @staticmethod
    def get_metadata(cb_name: str, model_version: str = "default", from_cache: bool = True) -> ModelMetadata:
        """
        Loads the metadata of a model for the given Codebook
        :param cb_name: the codebook name
        :param model_version: version tag of the model (e.g. "default")
        :param from_cache: if True return metadata from Redis cache otherwise from physical file
        :return: the metadata of the model for the given Codebook
        """
        try:
            if from_cache:
                return RedisHandler().get_model_metadata(cb_name, model_version)
            else:
                return DataHandler.get_model_metadata(cb_name, model_version)
        except Exception:
            raise ModelNotAvailableException(cb_name=cb_name, model_version="default")

    @staticmethod
    def publish_model(r: TrainingRequest, eval_results: Dict[str, float]) -> ModelMetadata:

        backend_logger.info(f"Generating model metadata for model '{r.model_version}' of Codebook '{r.cb_name}'")

        dataset_metadata = DatasetManager.get_metadata(r.cb_name, r.dataset_version)

        metadata = ModelMetadata(
            codebook_name=r.cb_name,
            version=r.model_version,
            dataset_version=r.dataset_version,
            labels=dataset_metadata.labels,
            model_type='DNNClassifier',  # TODO
            evaluation=eval_results,
            model_config=r.model_config.dict()
        )

        DataHandler.store_model_metadata(r.cb_name, metadata)
        RedisHandler().register_model(r.cb_name, metadata)

        return metadata

    @staticmethod
    def store_uploaded_model(cb_name: str, model_version: str, model_archive: UploadFile) -> str:
        # TODO register in redis
        # - create metadata for model or make sure it exists in the archive
        backend_logger.info(f"Successfully received model archive for Codebook {cb_name}")
        try:
            path = DataHandler.store_model(cb_name, model_archive, model_version)
        except Exception as e:
            raise ErroneousModelException(model_version, cb_name,
                                          f"Error while persisting model for Codebook {cb_name}!")
        if not ModelManager.is_available(cb_name):
            raise ErroneousModelException(model_version, cb_name,
                                          f"Archive contains no valid model for Codebook {cb_name} under {path}!")
        backend_logger.info(
            f"Successfully persisted model '{model_version}' for Codebook <{cb_name}> under {path}!")
        return str(path)

    @staticmethod
    def remove(cb_name: str, model_version: str):
        try:
            backend_logger.info(f"Removing model '{model_version}' of Codebook {cb_name}")
            RedisHandler().unregister_model(cb_name, model_version)
            DataHandler.purge_model_directory(cb_name, model_version)
            return True
        except Exception as e:
            return False


    @staticmethod
    def list_models(cb_name) -> List[ModelMetadata]:
        try:
            return RedisHandler().list_models(cb_name)
        except Exception as e:
            return []

    @staticmethod
    def build_model_id(cb_name: str, model_version: str = "default", dataset_version: str = "default") -> str:
        mid = cb_name + "_mv_" + model_version + "_dv_" + dataset_version
        assert ModelManager._is_valid_model_id(mid)
        return mid

    @staticmethod
    def _is_valid_model_id(model_id: str) -> bool:
        # name_hash_m_modelVersion_d_datasetVersion
        model_id_pattern = re.compile(r"[A-Za-z0-9]+_mv_[A-Za-z0-9]+_dv_[A-Za-z0-9]+")
        if not model_id_pattern.match(model_id):
            raise InvalidModelIdException(model_id)
        else:
            return True

    @staticmethod
    def parse_model_id(model_id: str) -> Tuple[str, str, str]:
        assert ModelManager._is_valid_model_id(model_id)
        data = model_id.split("_")
        cb_name = data[0]
        model_version = data[2]
        dataset_version = data[4]
        return cb_name, model_version, dataset_version
