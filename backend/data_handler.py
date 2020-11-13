import hashlib
import json
import os
import shutil
import zipfile
from pathlib import Path
from zipfile import ZipFile

from fastapi import UploadFile

from api.model import CodebookModel
from logger import backend_logger
from .exceptions import DatasetNotAvailableException
from .exceptions import ModelNotAvailableException
from .exceptions import NoDataForCodebookException


class DataHandler(object):
    _singleton = None
    _DATA_BASE_PATH: Path = None
    _relative_dataset_directory: Path = Path("dataset/")
    _relative_model_directory: Path = Path("model/")

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
            cls._DATA_BASE_PATH = Path(env_var)

            # create the BASE_PATH if it doesn't exist
            if not cls._DATA_BASE_PATH.exists():
                cls._DATA_BASE_PATH.mkdir(parents=True)

        return cls._singleton

    @staticmethod
    def get_data_handle(cb: CodebookModel) -> str:
        """
        Computes the data handle for the given Codebook by MD5-hashing it's JSON representation (after sorting tags).
        Note that this is just an identifier / handle that does not guarantee that data for the Codebook exists.
        :param cb: The codebook model!
        :return: The data handle as a string
        """
        cb.tags.sort()
        return hashlib.md5(cb.json().encode('utf-8')).hexdigest()

    @staticmethod
    def get_model_directory(cb: CodebookModel, model_version: str = "default", create: bool = False) -> Path:
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
    def get_model_dir_from_handle(cb_data_handle: str, model_version: str = "default", create: bool = False) -> Path:
        model_version = "default" if model_version is None or model_version == "" else model_version
        # TODO exception if data dir not available
        model_dir = DataHandler._get_data_dir_from_handle(cb_data_handle=cb_data_handle).joinpath(
            DataHandler._relative_model_directory).joinpath(model_version)
        if create:
            model_dir.mkdir(exist_ok=True, parents=True)
        if not model_dir.is_dir():
            # TODO add model id or cb for proper error msg
            raise ModelNotAvailableException()
        return model_dir

    @staticmethod
    def store_dataset(cb: CodebookModel, dataset_archive: UploadFile, dataset_version: str) -> Path:
        try:
            ds_dir = DataHandler.get_dataset_directory(cb, dataset_version=dataset_version, create=True)
            dst = ds_dir.joinpath(dataset_archive.filename)
            archive_path = DataHandler._store_uploaded_file(dataset_archive, dst)
            return DataHandler._extract_archive(archive=archive_path, dst=ds_dir)
        finally:
            dataset_archive.file.close()

    @staticmethod
    def store_model(cb: CodebookModel, model_archive: UploadFile, model_version: str) -> Path:
        try:
            ds_dir = DataHandler.get_model_directory(cb, model_version=model_version, create=True)
            dst = ds_dir.joinpath(model_archive.filename)
            archive_path = DataHandler._store_uploaded_file(model_archive, dst)
            return DataHandler._extract_archive(archive=archive_path, dst=ds_dir)
        finally:
            model_archive.file.close()

    @staticmethod
    def get_dataset_directory(cb: CodebookModel, dataset_version: str = "default", create: bool = False) -> Path:
        data_directory = DataHandler._get_data_directory(cb, create).joinpath(
            DataHandler._relative_dataset_directory).joinpath(
            dataset_version)
        if create:
            data_directory.mkdir(exist_ok=True, parents=True)
        if not data_directory.is_dir():
            raise DatasetNotAvailableException(dataset_version=dataset_version, cb=cb)
        return data_directory

    @staticmethod
    def _get_data_directory(cb: CodebookModel, create: bool = False) -> Path:
        data_handle = DataHandler.get_data_handle(cb)
        data_directory = Path(DataHandler._DATA_BASE_PATH, data_handle)
        if create:
            data_directory.mkdir(exist_ok=True, parents=True)
        if not data_directory.is_dir():
            raise NoDataForCodebookException(cb=cb)
        return data_directory

    @staticmethod
    def _get_data_dir_from_handle(cb_data_handle: str) -> Path:
        data_directory = Path(DataHandler._DATA_BASE_PATH, cb_data_handle)
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
