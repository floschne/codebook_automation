import json
import os
from pathlib import Path

from fastapi import UploadFile

from api.model import CodebookModel
from backend import ModelManager
from backend.exceptions import ErroneousDatasetException
from logger import backend_logger
from .data_handler import DataHandler


class Trainer(object):
    _singleton = None

    def __new__(cls, *args, **kwargs):
        if cls._singleton is None:
            backend_logger.info('Instantiating Trainer!')

            # load config file
            config = json.load(open("config.json", "r"))

            # make sure GPU is available for ModelTrainer (if there is one)
            if not bool(config['backend']['use_gpu_for_training']):
                backend_logger.info("GPU support for training disabled!")
                os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
            else:
                backend_logger.info("GPU support for training enabled!")

            cls._singleton = super(Trainer, cls).__new__(cls)
            cls._dh = DataHandler()
            cls._mm = ModelManager()

        return cls._singleton

    def store_uploaded_dataset(self, cb: CodebookModel, dataset_version: str, dataset_archive: UploadFile) -> Path:
        # TODO
        # - make sure that a valid CSV dataset was extracted -> dataset_is_available
        backend_logger.info(f"Successfully received dataset archive for Codebook {cb.name}")

        try:
            path = self._dh.store_dataset(cb=cb, dataset_archive=dataset_archive, dataset_version=dataset_version)
        except Exception as e:
            raise ErroneousDatasetException(dataset_version, cb,
                                            f"Error while persisting dataset for Codebook {cb.name}!",
                                            caused_by=str(e))
        if not self.dataset_is_available(cb, dataset_version=dataset_version):
            raise ErroneousDatasetException(dataset_version, cb,
                                            f"Error while persisting dataset for Codebook {cb.name} under {str(path)}")
        backend_logger.info(
            f"Successfully persisted dataset '{dataset_version}' for Codebook <{cb.name}> under {str(path)}")
        return path

    @staticmethod
    def dataset_is_available(cb: CodebookModel, dataset_version: str) -> bool:
        return True
