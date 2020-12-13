import json
import re
from pathlib import Path
from typing import Tuple

import tensorflow as tf
from fastapi import UploadFile

from api.model import CodebookModel, ModelMetadata
from logger import backend_logger
from .data_handler import DataHandler
from .exceptions import ErroneousModelException, ModelMetadataNotAvailableException, ModelNotAvailableException, \
    NoDataForCodebookException, InvalidModelIdException


class ModelManager(object):
    _singleton = None

    def __new__(cls, *args, **kwargs):
        if cls._singleton is None:
            backend_logger.info('Instantiating ModelManager!')
            cls._singleton = super(ModelManager, cls).__new__(cls)
        return cls._singleton

    @staticmethod
    def is_available(cb: CodebookModel, model_version: str = "default") -> bool:
        """
        Checks if the model for the given codebook is available
        :param cb: the codebook
        :param model_version: version tag of the model (e.g. "default")
        :return: True if the model for the codebook is available and False otherwise
        """
        try:
            model_dir = DataHandler.get_model_directory(cb, model_version=model_version)
            return tf.saved_model.contains_saved_model(model_dir)
        except (ModelMetadataNotAvailableException, ModelNotAvailableException, NoDataForCodebookException) as e:
            return False

    @staticmethod
    def load(cb: CodebookModel, model_version: str = "default"):
        """
        Loads the Tensorflow Estimator model for the given Codebook
        :param cb: the codebook
        :param model_version: version tag of the model (e.g. "default")
        :return: the Tensorflow Estimator model for the given Codebook
        """
        model_dir = DataHandler.get_model_directory(cb, model_version=model_version)
        estimator = tf.saved_model.load(str(model_dir))
        if estimator.signatures["predict"] is None:
            raise ErroneousModelException(
                msg=f"Estimator / Model of version '{model_version}' for Codebook %s is erroneous!" % cb.name)

        return estimator

    @staticmethod
    def load_metadata(cb: CodebookModel, model_version: str = "default") -> ModelMetadata:
        # TODO merge with get_metadata_path()
        """
        Loads the metadata of a model for the given Codebook
        :param cb: the codebook
        :param model_version: version tag of the model (e.g. "default")
        :return: the metadata of the model for the given Codebook
        """
        # TODO
        #  - load from redis
        #  - outsource model meta data path etc
        model_dir = DataHandler.get_model_directory(cb, model_version=model_version)
        meta_data_path = model_dir.joinpath("assets.extra", "model_metadata.json")
        try:
            with open(meta_data_path, 'r') as json_file:
                data = json.load(json_file)
                return ModelMetadata(**data)
        except Exception:
            raise ModelMetadataNotAvailableException(cb=cb, model_version="default")

    @staticmethod
    def get_metadata_path(model_id: str, create: bool = False) -> Path:
        # TODO redis
        cb_id, model_version, _ = ModelManager.parse_model_id(model_id)
        model_dir = DataHandler.get_model_dir_from_id(cb_id=cb_id,
                                                      model_version=model_version,
                                                      create=create)
        metadata_path = model_dir.joinpath("metadata.json")
        if create:
            metadata_path.touch(exist_ok=True)
        return metadata_path

    @staticmethod
    def store_uploaded_model(cb: CodebookModel, model_version: str, model_archive: UploadFile) -> str:
        # TODO register in redis
        # - create metadata for model or make sure it exists in the archive
        backend_logger.info(f"Successfully received model archive for Codebook {cb.name}")
        try:
            path = DataHandler.store_model(cb, model_archive, model_version)
        except Exception as e:
            raise ErroneousModelException(model_version, cb,
                                          f"Error while persisting model for Codebook {cb.name}!")
        if not ModelManager.is_available(cb):
            raise ErroneousModelException(model_version, cb,
                                          f"Archive contains no valid model for Codebook {cb.name} under {path}!")
        backend_logger.info(
            f"Successfully persisted model '{model_version}' for Codebook <{cb.name}> under {path}!")
        return str(path)

    @staticmethod
    def remove(cb: CodebookModel, model_version: str):
        # TODO unregister
        backend_logger.info(f"Removing model '{model_version}' of Codebook {cb.name}")
        DataHandler.purge_model_directory(cb, model_version)
        return True

    @staticmethod
    def get_model_id(cb: CodebookModel, model_version: str = "default", dataset_version: str = "default") -> str:
        mid = cb._id + "_m_" + model_version + "_d_" + dataset_version
        assert ModelManager._is_valid_model_id(mid)
        return mid

    @staticmethod
    def _is_valid_model_id(model_id: str) -> bool:
        # name_hash_m_modelVersion_d_datasetVersion
        model_id_pattern = re.compile(r"[a-z0-9]+_[a-f0-9]{32}_m_[A-za-z0-9]+_d_[A-za-z0-9]+")
        if not model_id_pattern.match(model_id):
            raise InvalidModelIdException(model_id)
        else:
            return True

    @staticmethod
    def parse_model_id(model_id: str) -> Tuple[str, str, str]:
        assert ModelManager._is_valid_model_id(model_id)
        data = model_id.split("_")
        cb_id = data[0] + "_" + data[1]
        model_version = data[3]
        dataset_version = data[5]
        return cb_id, model_version, dataset_version
