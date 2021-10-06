from typing import List, Union

import redis
from loguru import logger as log

from api.model import ModelMetadata, DatasetMetadata, TagLabelMapping
from backend.exceptions import ModelNotAvailableException, DatasetNotAvailableException, \
    TagLabelMappingNotAvailableException, RedisError
from config import conf


class RedisHandler(object):
    _singleton = None
    __datasets: redis.Redis = None
    __models: redis.Redis = None
    __model_db_idx: int = 1
    __dataset_db_idx: int = 2
    __mapping_db_idx: int = 3

    def __new__(cls, *args, **kwargs):
        if cls._singleton is None:
            log.info('Instantiating RedisHandler!')
            cls._singleton = super(RedisHandler, cls).__new__(cls)

            # setup redis
            r_host = conf.backend.redis.host
            r_port = int(conf.backend.redis.port)
            assert r_host is not None and r_host != "", f"Redis Host not set!"
            assert r_port is not None and r_port >= 0, f"Redis Port not set!"

            cls.__datasets = redis.Redis(host=r_host, port=r_port, db=cls.__dataset_db_idx)
            assert cls.__datasets.ping(), f"Couldn't connect to Redis DB {cls.__dataset_db_idx} at {r_host}:{r_port}!"
            cls.__models = redis.Redis(host=r_host, port=r_port, db=cls.__model_db_idx)
            assert cls.__models.ping(), f"Couldn't connect to Redis DB {cls.__model_db_idx} at {r_host}:{r_port}!"
            cls.__mappings = redis.Redis(host=r_host, port=r_port, db=cls.__mapping_db_idx)
            assert cls.__mappings.ping(), f"Couldn't connect to Redis DB {cls.__model_db_idx} at {r_host}:{r_port}!"

        return cls._singleton

    @staticmethod
    def __filter_by_version(cb_name: str,
                            metadata: List[Union[ModelMetadata, DatasetMetadata, TagLabelMapping]],
                            version: str) -> Union[ModelMetadata, DatasetMetadata, None]:
        # TODO think of using Redis Indices (ZADD) and index by version
        def filter_fn(m: Union[ModelMetadata, DatasetMetadata, TagLabelMapping]):
            return m.version == version

        filtered = list(filter(filter_fn, metadata))
        if len(filtered) != 1 or len(metadata) == 0:
            if isinstance(metadata[0], ModelMetadata):
                raise ModelNotAvailableException(cb_name=cb_name, model_version=version)
            elif isinstance(metadata[0], DatasetMetadata):
                raise DatasetNotAvailableException(cb_name=cb_name, dataset_version=version)
            elif isinstance(metadata[0], TagLabelMapping):
                raise TagLabelMappingNotAvailableException(cb_name=cb_name, model_version=version)
        return filtered[0]

    def register_model(self, cb_name: str, metadata: ModelMetadata):
        if not self.__models.sadd(cb_name, metadata.json()) == 1:
            raise RedisError(f"Error while registering model '{metadata.version}' of Codebook '{cb_name}'!")
        log.info(f"Successfully registered model '{metadata.version}' of Codebook '{cb_name}'!")

    def register_dataset(self, cb_name: str, metadata: DatasetMetadata):
        if not self.__datasets.sadd(cb_name, metadata.json()) == 1:
            raise RedisError(f"Error while registering dataset '{metadata.version}' of Codebook '{cb_name}'!")
        log.info(f"Successfully registered dataset '{metadata.version}' of Codebook '{cb_name}'!")

    def register_mapping(self, cb_name: str, mapping: TagLabelMapping):
        if not self.__mappings.sadd(cb_name, mapping.json()) == 1:
            raise RedisError(
                f"Error while registering TagLabelMapping for Codebook '{cb_name}' and model version '{mapping.version}'!")
        log.info(
            f"Successfully registered TagLabelMapping for Codebook '{cb_name}' and model version '{mapping.version}'!")

    def unregister_model(self, cb_name: str, model_version: str):
        metadata = self.get_model_metadata(cb_name, model_version)
        if not self.__models.srem(cb_name, metadata.json()) == 1:
            raise RedisError(f"Error while unregistering model '{model_version}' of Codebook '{cb_name}'!")
        log.info(f"Successfully unregistered model '{model_version}' of Codebook '{cb_name}'!")

    def unregister_dataset(self, cb_name: str, dataset_version: str):
        metadata = self.get_dataset_metadata(cb_name, dataset_version)
        if not self.__datasets.srem(cb_name, metadata.json()) == 1:
            raise RedisError(f"Error while unregistering dataset '{dataset_version}' of Codebook '{cb_name}'")
        log.info(f"Successfully unregistered dataset '{dataset_version}' of Codebook '{cb_name}'")

    def unregister_mapping(self, cb_name: str, model_version: str):
        mapping = self.get_mapping(cb_name, model_version)
        assert self.__mappings.srem(cb_name, mapping.json()) == 1
        log.info(f"Successfully unregistered TagLabelMapping '{model_version}' of Codebook '{cb_name}'!")

    def get_model_metadata(self, cb_name: str, model_version: str) -> ModelMetadata:
        m = self.list_models(cb_name)
        if len(m) == 0:
            raise ModelNotAvailableException(model_version=model_version, cb_name=cb_name)
        return self.__filter_by_version(cb_name, m, model_version)

    def get_dataset_metadata(self, cb_name: str, dataset_version: str) -> DatasetMetadata:
        m = self.list_datasets(cb_name)
        if len(m) == 0:
            raise DatasetNotAvailableException(dataset_version=dataset_version, cb_name=cb_name)
        return self.__filter_by_version(cb_name, m, dataset_version)

    def get_mapping(self, cb_name: str, model_version: str):
        m = self.list_mappings(cb_name)
        if len(m) == 0:
            raise TagLabelMappingNotAvailableException(model_version=model_version, cb_name=cb_name)
        return self.__filter_by_version(cb_name, m, model_version)

    def list_mappings(self, cb_name: str) -> List[TagLabelMapping]:
        mappings = self.__mappings.smembers(cb_name)
        return [TagLabelMapping.parse_raw(m) for m in mappings]

    def list_models(self, cb_name: str) -> List[ModelMetadata]:
        models = self.__models.smembers(cb_name)
        return [ModelMetadata.parse_raw(m) for m in models]

    def list_datasets(self, cb_name: str) -> List[DatasetMetadata]:
        datasets = self.__datasets.smembers(cb_name)
        return [DatasetMetadata.parse_raw(m) for m in datasets]
