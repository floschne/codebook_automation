import json
import os
from typing import List, Union

import redis

from api.model import ModelMetadata, DatasetMetadata
from backend.exceptions import ModelNotAvailableException, DatasetNotAvailableException
from logger import backend_logger


class RedisHandler(object):
    _singleton = None
    __datasets: redis.Redis = None
    __models: redis.Redis = None
    __model_db_idx: int = 1
    __dataset_db_idx: int = 2

    def __new__(cls, *args, **kwargs):
        if cls._singleton is None:
            backend_logger.info('Instantiating RedisHandler!')
            cls._singleton = super(RedisHandler, cls).__new__(cls)

            # setup redis
            config = json.load(open("config/config.json", "r"))
            # TODO maybe create separate handler for redis and enable config of:
            #  - user & pw
            #  - SSL
            #  - TTL
            #  - omegaconf
            host_env_var = config['backend']['redis']['host_env_var'].strip()
            port_env_var = config['backend']['redis']['port_env_var'].strip()
            r_host = os.getenv(host_env_var, None)
            r_port = os.getenv(port_env_var, None)
            assert r_host is not None and r_host != "", f"{host_env_var} environment variable not set!"
            assert r_port is not None, f"{port_env_var} environment variable not set!"

            cls.__datasets = redis.Redis(host=r_host, port=r_port, db=cls.__dataset_db_idx)
            assert cls.__datasets.ping(), f"Couldn't connect to Redis DB {cls.__dataset_db_idx} at {r_host}:{r_port}!"
            cls.__models = redis.Redis(host=r_host, port=r_port, db=cls.__model_db_idx)
            assert cls.__models.ping(), f"Couldn't connect to Redis DB {cls.__model_db_idx} at {r_host}:{r_port}!"

        return cls._singleton

    @staticmethod
    def __filter_by_version(cb_name: str, metadata: List[Union[ModelMetadata, DatasetMetadata]], version: str) \
            -> Union[ModelMetadata, DatasetMetadata, None]:
        if len(metadata) == 0:
            return None

        # TODO think of using Redis Indices (ZADD) and index by version
        def filter_fn(md: Union[ModelMetadata, DatasetMetadata]):
            return md.version == version

        filtered = list(filter(filter_fn, metadata))
        if len(filtered) != 1 and len(metadata) > 0:
            if isinstance(metadata[0], ModelMetadata):
                raise ModelNotAvailableException(cb_name=cb_name, model_version=version)
            elif isinstance(metadata[0], DatasetMetadata):
                raise DatasetNotAvailableException(cb_name=cb_name, dataset_version=version)
        return filtered[0]

    def register_model(self, cb_name: str, metadata: ModelMetadata):
        assert self.__models.sadd(cb_name, metadata.json()) == 1
        backend_logger.info(f"Successfully registered model '{metadata.version}' of Codebook '{cb_name}'!")

    def register_dataset(self, cb_name: str, metadata: DatasetMetadata):
        assert self.__datasets.sadd(cb_name, metadata.json()) == 1
        backend_logger.info(
            f"Successfully registered dataset '{metadata.version}' of Codebook '{cb_name}'!")

    def unregister_model(self, cb_name: str, model_version: str):
        metadata = self.get_model_metadata(cb_name, model_version)
        assert self.__models.srem(cb_name, metadata.json()) == 1
        backend_logger.info(f"Successfully unregistered model '{model_version}' of Codebook '{cb_name}'!")

    def unregister_dataset(self, cb_name: str, dataset_version: str):
        metadata = self.get_dataset_metadata(cb_name, dataset_version)
        assert self.__datasets.srem(cb_name, metadata.json()) == 1
        backend_logger.info(f"Successfully unregistered dataset '{dataset_version}' of Codebook '{cb_name}'")

    def get_model_metadata(self, cb_name: str, model_version: str) -> ModelMetadata:
        return self.__filter_by_version(cb_name, self.list_models(cb_name), model_version)

    def get_dataset_metadata(self, cb_name: str, dataset_version: str) -> DatasetMetadata:
        return self.__filter_by_version(cb_name, self.list_datasets(cb_name), dataset_version)

    def list_models(self, cb_name: str) -> List[ModelMetadata]:
        models = self.__models.smembers(cb_name)
        return [ModelMetadata.parse_raw(m) for m in models]

    def list_datasets(self, cb_name: str) -> List[DatasetMetadata]:
        datasets = self.__datasets.smembers(cb_name)
        return [DatasetMetadata.parse_raw(m) for m in datasets]
