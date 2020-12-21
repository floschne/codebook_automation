import json
from typing import List, Union

import redis

from api.model import ModelMetadata, DatasetMetadata
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
            config = json.load(open("config.json", "r"))
            # TODO maybe create separate handler for redis and enable config of:
            #  - user & pw
            #  - SSL
            #  - TTL
            r_host = config['backend']['redis']['host']
            r_port = config['backend']['redis']['port']
            cls.__datasets = redis.Redis(host=r_host, port=r_port, db=cls.__dataset_db_idx)
            assert cls.__datasets.ping(), f"Couldn't connect to Redis DB {cls.__dataset_db_idx} at {r_host}:{r_port}!"
            cls.__models = redis.Redis(host=r_host, port=r_port, db=cls.__model_db_idx)
            assert cls.__models.ping(), f"Couldn't connect to Redis DB {cls.__model_db_idx} at {r_host}:{r_port}!"

        return cls._singleton

    @staticmethod
    def __filter_by_version(metadata: List[Union[ModelMetadata, DatasetMetadata]], version: str) \
            -> Union[ModelMetadata, DatasetMetadata]:
        # TODO think of using Redis Indices (ZADD) and index by version
        def filter_fn(md: Union[ModelMetadata, DatasetMetadata]):
            return md.version == version

        filtered = list(filter(filter_fn, metadata))
        assert len(filtered) == 1
        return filtered[0]

    @staticmethod
    def register_model(cb_name: str, metadata: ModelMetadata):
        assert RedisHandler.__models.sadd(cb_name, metadata.json()) == 1

    @staticmethod
    def register_dataset(cb_name: str, metadata: DatasetMetadata):
        assert RedisHandler.__datasets.sadd(cb_name, metadata.json()) == 1

    @staticmethod
    def get_model_metadata(cb_name: str, model_version: str) -> ModelMetadata:
        return RedisHandler.__filter_by_version(RedisHandler.list_models(cb_name), model_version)

    @staticmethod
    def get_dataset_metadata(cb_name: str, dataset_version: str) -> DatasetMetadata:
        return RedisHandler.__filter_by_version(RedisHandler.list_models(cb_name), dataset_version)

    @staticmethod
    def list_models(cb_name: str) -> List[ModelMetadata]:
        models = RedisHandler.__models.smembers(cb_name)
        return [ModelMetadata.parse_raw(m) for m in models]

    @staticmethod
    def list_datasets(cb_name: str) -> List[DatasetMetadata]:
        datasets = RedisHandler.__datasets.smembers(cb_name)
        return [DatasetMetadata.parse_raw(m) for m in datasets]

    @staticmethod
    def unregister_model(cb_name: str, model_version: str):
        model_metadata = RedisHandler.get_model_metadata(cb_name, model_version)
        assert RedisHandler.__models.srem(cb_name, model_metadata) == 1

    @staticmethod
    def unregister_dataset(cb_name: str, dataset_version: str):
        model_metadata = RedisHandler.get_dataset_metadata(cb_name, dataset_version)
        assert RedisHandler.__models.srem(cb_name, model_metadata) == 1
