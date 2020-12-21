import json
import os
import shutil
import zipfile
from pathlib import Path
from zipfile import ZipFile

from fastapi import UploadFile

from api.model import CodebookDTO, DatasetMetadata, ModelMetadata
from logger import backend_logger
from .exceptions import DatasetNotAvailableException
from .exceptions import ModelNotAvailableException
from .exceptions import NoDataForCodebookException


class DataHandler(object):
    _singleton = None
    _DATA_ROOT: Path = None
    _relative_dataset_directory: Path = Path("dataset/")
    _relative_model_directory: Path = Path("model/")
    _redis = None

    def __new__(cls, *args, **kwargs):
        if cls._singleton is None:
            backend_logger.info('Instantiating DataHandler!')
            cls._singleton = super(DataHandler, cls).__new__(cls)

            # read the data base path from config and 'validate' it
            config = json.load(open("config.json", "r"))
            env_var = config['backend']['data_base_path_env_var']
            env_var = os.getenv(env_var, None)
            assert env_var is not None and env_var != "", "DATA_BASE_PATH environment variable not set!"
            env_var = env_var.strip()
            cls._DATA_ROOT = Path(env_var)

            # create the BASE_PATH if it doesn't exist
            if not cls._DATA_ROOT.exists():
                cls._DATA_ROOT.mkdir(parents=True)

        return cls._singleton

    @staticmethod
    def get_model_directory(cb: CodebookDTO, model_version: str = "default", create: bool = False) -> Path:
        model_version = "default" if model_version is None or model_version == "" else model_version
        model_dir = DataHandler._get_data_directory(cb, create).joinpath(
            DataHandler._relative_model_directory).joinpath(
            model_version)
        if create:
            model_dir.mkdir(exist_ok=True, parents=True)
        if not model_dir.is_dir():
            raise ModelNotAvailableException(model_version=model_version, cb=cb)
        return model_dir

    @staticmethod
    def get_model_dir_from_id(cb_id: str, model_version: str = "default", create: bool = False) -> Path:
        model_version = "default" if model_version is None or model_version == "" else model_version
        # TODO exception if data dir not available
        model_dir = DataHandler._get_data_dir_from_id(cb_id=cb_id).joinpath(
            DataHandler._relative_model_directory).joinpath(model_version)
        if create:
            model_dir.mkdir(exist_ok=True, parents=True)
        if not model_dir.is_dir():
            # TODO add model id or cb for proper error msg
            raise ModelNotAvailableException()
        return model_dir

    @staticmethod
    def store_dataset(cb: CodebookDTO, dataset_archive: UploadFile, dataset_version: str) -> Path:
        try:
            ds_dir = DataHandler.get_dataset_directory(cb, dataset_version=dataset_version, create=True)
            dst = ds_dir.joinpath(dataset_archive.filename)
            backend_logger.info(f"Extracting dataset archive to {str(dst)}")
            archive_path = DataHandler._store_uploaded_file(dataset_archive, dst)
            return DataHandler._extract_archive(archive=archive_path, dst=ds_dir)
        finally:
            dataset_archive.file.close()

    @staticmethod
    def store_dataset_metadata(cb: CodebookDTO, dataset_metadata: DatasetMetadata) -> Path:
        ds_dir = DataHandler.get_dataset_directory(cb, dataset_version=dataset_metadata.version, create=False)
        dst = ds_dir.joinpath('metadata.json')
        with open(dst, 'w') as out:
            backend_logger.info(f"Storing dataset metadata at {str(dst)}")
            print(dataset_metadata.json(), file=out)
        assert dst.exists() and DatasetMetadata.parse_file(dst) == dataset_metadata  # TODO exception
        return dst

    @staticmethod
    def store_model(cb: CodebookDTO, model_archive: UploadFile, model_version: str) -> Path:
        try:
            model_dir = DataHandler.get_model_directory(cb, model_version=model_version, create=True)
            dst = model_dir.joinpath(model_archive.filename)
            backend_logger.info(f"Extracting model archive to {str(dst)}")
            archive_path = DataHandler._store_uploaded_file(model_archive, dst)
            return DataHandler._extract_archive(archive=archive_path, dst=model_dir)
        finally:
            model_archive.file.close()

    @staticmethod
    def store_model_metadata(cb: CodebookDTO, model_metadata: ModelMetadata) -> Path:
        model_dir = DataHandler.get_model_directory(cb, model_version=model_metadata.model_version, create=False)
        dst = model_dir.joinpath('metadata.json')
        with open(dst, 'w') as out:
            backend_logger.info(f"Storing model metadata at {str(dst)}")
            print(model_metadata.json(), file=out)
        assert dst.exists() and ModelMetadata.parse_file(dst) == model_metadata  # TODO exception
        return dst

    @staticmethod
    def get_dataset_directory(cb: CodebookDTO, dataset_version: str = "default", create: bool = False) -> Path:
        data_directory = DataHandler._get_data_directory(cb, create).joinpath(
            DataHandler._relative_dataset_directory).joinpath(
            dataset_version)
        if create:
            data_directory.mkdir(exist_ok=True, parents=True)
        if not data_directory.is_dir():
            raise DatasetNotAvailableException(dataset_version=dataset_version, cb=cb)
        return data_directory

    @staticmethod
    def _get_data_directory(cb: CodebookDTO, create: bool = False) -> Path:
        data_directory = Path(DataHandler._DATA_ROOT, cb.id)
        if create:
            data_directory.mkdir(exist_ok=True, parents=True)
        if not data_directory.is_dir():
            raise NoDataForCodebookException(cb=cb)
        return data_directory

    @staticmethod
    def _get_data_dir_from_id(cb_id: str) -> Path:
        data_directory = Path(DataHandler._DATA_ROOT, cb_id)
        assert data_directory.is_dir()
        return data_directory

    @staticmethod
    def _extract_archive(archive: Path, dst: Path):
        assert zipfile.is_zipfile(archive)
        with ZipFile(archive, 'r') as zip_archive:
            zip_archive.extractall(dst)
        assert dst.is_dir()
        return dst

    @staticmethod
    def _store_uploaded_file(uploaded_file: UploadFile, dst: Path):
        with open(dst, "wb") as buffer:
            shutil.copyfileobj(uploaded_file.file, buffer)
            return Path(dst)

    @staticmethod
    def purge_dataset_directory(cb: CodebookDTO, dataset_version: str):
        dataset_dir = DataHandler.get_dataset_directory(cb, dataset_version=dataset_version)
        backend_logger.warning(f"Permanently removing dataset '{dataset_version}' of Codebook '{cb.name}'")
        shutil.rmtree(dataset_dir)

    @staticmethod
    def purge_model_directory(cb: CodebookDTO, model_version: str):
        model_dir = DataHandler.get_model_directory(cb, model_version=model_version)
        backend_logger.warning(f"Permanently removing data of model '{model_version}' of Codebook '{cb.name}'")
        shutil.rmtree(model_dir)

    @staticmethod
    def _purge_data(cb: CodebookDTO):
        backend_logger.warning(
            f"Permanently removing all data (including models and datasets) of Codebook <{cb.name}>!")
        data_directory = Path(DataHandler._DATA_ROOT, cb.id)
        shutil.rmtree(data_directory)
