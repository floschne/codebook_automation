import json

import tensorflow as tf
from fastapi import UploadFile

from api.model import CodebookModel, ModelMetadata
from backend.exceptions import ErroneousModelException, ModelMetadataNotAvailableException
from logger import backend_logger
from .data_handler import DataHandler


class ModelManager(object):
    _singleton = None

    def __new__(cls, *args, **kwargs):
        if cls._singleton is None:
            cls._dh = DataHandler()

            backend_logger.info('Instantiating ModelManager!')
            cls._singleton = super(ModelManager, cls).__new__(cls)
        return cls._singleton

    def model_is_available(self, cb: CodebookModel, model_version: str = "default") -> bool:
        """
        Checks if the model for the given codebook is available
        :param cb: the codebook
        :param model_version: version tag of the model (e.g. "default")
        :return: True if the model for the codebook is available and False otherwise
        """
        model_dir = self._dh.get_model_directory(cb, model_version=model_version)
        return tf.saved_model.contains_saved_model(model_dir)

    def load_estimator(self, cb: CodebookModel, model_version: str = "default"):
        """
        Loads the Tensorflow Estimator model for the given Codebook
        :param cb: the codebook
        :param model_version: version tag of the model (e.g. "default")
        :return: the Tensorflow Estimator model for the given Codebook
        """
        model_dir = self._dh.get_model_directory(cb, model_version=model_version)
        estimator = tf.saved_model.load(str(model_dir))
        if estimator.signatures["predict"] is None:
            raise ErroneousModelException(
                msg=f"Estimator / Model of version '{model_version}' for Codebook %s is erroneous!" % cb.name)

        return estimator

    def load_model_metadata(self, cb: CodebookModel, model_version: str = "default") -> ModelMetadata:
        """
        Loads the metadata of a model for the given Codebook
        :param cb: the codebook
        :param model_version: version tag of the model (e.g. "default")
        :return: the metadata of the model for the given Codebook
        """
        # TODO
        # - outsource model meta data path etc
        model_dir = self._dh.get_model_directory(cb, model_version=model_version)
        meta_data_path = model_dir.joinpath("assets.extra", "model_metadata.json")
        try:
            with open(meta_data_path, 'r') as json_file:
                data = json.load(json_file)
                return ModelMetadata(**data)
        except Exception:
            raise ModelMetadataNotAvailableException(cb=cb, model_version="default")

    def store_uploaded_model(self, cb: CodebookModel, model_version: str, model_archive: UploadFile) -> str:
        # TODO
        # - make sure that a valid TF model was extracted
        # - create metadata for model or make sure it exists in the archive
        backend_logger.info(f"Successfully received model archive for Codebook {cb.name}")
        try:
            path = self._dh.store_model(cb, model_archive, model_version)
        except Exception as e:
            raise ErroneousModelException(model_version, cb,
                                          f"Error while persisting model for Codebook {cb.name}!")
        if not self.model_is_available(cb):
            raise ErroneousModelException(model_version, cb,
                                          f"Error while persisting model for Codebook {cb.name} under {path}!")
        backend_logger.info(
            f"Successfully persisted model '{model_version}' for Codebook <{cb.name}> under {path}!")
        return str(path)
