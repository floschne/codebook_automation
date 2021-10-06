from typing import Union, Tuple, List

import numpy as np
import pandas as pd
import tensorflow as tf
from fastapi import UploadFile
from loguru import logger as log

from api.model import DatasetMetadata
from backend.data_handler import DataHandler
from backend.db.redis_handler import RedisHandler
from backend.exceptions import ErroneousDatasetException, DatasetNotAvailableException


class DatasetManager(object):
    _singleton = None

    def __new__(cls, *args: object, **kwargs: object):
        if cls._singleton is None:
            log.info('Instantiating DatasetManager!')
            cls._singleton = super(DatasetManager, cls).__new__(cls)
        return cls._singleton

    @staticmethod
    def store_archive(cb_name: str, dataset_version: str, dataset_archive: UploadFile) -> DatasetMetadata:
        log.info(f"Successfully received dataset archive for Codebook {cb_name}")

        try:
            path = DataHandler.store_dataset(cb_name=cb_name, dataset_archive=dataset_archive,
                                             dataset_version=dataset_version)
            metadata = DatasetManager._generate_metadata(cb_name=cb_name, dataset_version=dataset_version)
            metadata_path = DataHandler.store_dataset_metadata(cb_name=cb_name, dataset_metadata=metadata)
        except Exception as e:
            raise ErroneousDatasetException(dataset_version, cb_name,
                                            f"Error while persisting dataset '{dataset_version}' for Codebook {cb_name}!",
                                            caused_by=str(e))

        RedisHandler().register_dataset(cb_name, metadata)
        log.info(
            f"Successfully persisted dataset '{dataset_version}' for Codebook <{cb_name}> under {str(path)} and "
            f"metadata under {metadata_path}")
        return metadata

    @staticmethod
    def get_tensorflow_dataset(cb_name: str, dataset_version: str = "default", get_labels_only=False) -> \
            Union[List[str], Tuple[tf.data.Dataset, tf.data.Dataset, List[str]]]:

        # load and prepare the dataframes
        train_df, test_df = DatasetManager._load_dataframes(cb_name, dataset_version)
        train_set, test_set, label_categories = DatasetManager._prepare_dataframes(train_df, test_df)
        if get_labels_only:
            return label_categories

        # extract label column
        train_labels = train_set.pop('label')
        test_labels = test_set.pop('label')

        # build tensorflow dataset
        train_ds = tf.data.Dataset.from_tensor_slices((train_set.values, train_labels.values))
        test_ds = tf.data.Dataset.from_tensor_slices((test_set.values, test_labels.values))

        # create dicts
        train_ds = train_ds.map(lambda features, labels: ({'text': features}, labels))
        test_ds = test_ds.map(lambda features, labels: ({'text': features}, labels))

        return train_ds, test_ds, label_categories

    @staticmethod
    def _prepare_dataframes(train_set: pd.DataFrame, test_set: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, List]:
        # convert to columns str
        train_set['text'] = train_set['text'].astype(str)
        test_set['text'] = train_set['text'].astype(str)
        train_set['label'] = train_set['label'].astype(str)
        test_set['label'] = train_set['label'].astype(str)

        # convert labels to categorical data
        # TODO maybe outsource label dict to file in dataset archive
        # FIXME in (hopefully) rare situations induced by the dataset designer,
        #  train_set could not contain all labels from test_set or vice versa...)
        train_cats = pd.Categorical(train_set['label'])
        test_cats = pd.Categorical(test_set['label'])
        # make sure labels are int32
        train_set['label'] = np.asarray(train_cats.codes, dtype=np.int32)
        test_set['label'] = np.asarray(test_cats.codes, dtype=np.int32)

        return train_set, test_set, list(train_cats.categories)

    @staticmethod
    def _load_dataframes(cb_name: str, dataset_version: str = "default") -> Tuple[pd.DataFrame, pd.DataFrame]:
        dataset_dir = DataHandler.get_dataset_directory(cb_name, dataset_version=dataset_version)

        # make sure train.csv & test.csv is available and has two columns 'text' & 'label'
        train_csv = dataset_dir.joinpath("train.csv")
        test_csv = dataset_dir.joinpath("test.csv")

        if not train_csv.exists() or not test_csv.exists():
            raise DatasetNotAvailableException(cb_name=cb_name, dataset_version=dataset_version)
        else:
            # TODO
            #  - this might be very inefficient for large datasets?!
            #  - use chunks for large datasets
            #  - use feather format (to_feather , read_feather)
            train_df = pd.read_csv(train_csv)
            test_df = pd.read_csv(test_csv)
            return train_df, test_df

    @staticmethod
    def _generate_metadata(cb_name: str, dataset_version: str = "default", ) -> DatasetMetadata:
        log.info(f"Generating dataset '{dataset_version}' metadata file for Codebook <{cb_name}>")
        # load and prepare the dataframes
        train_df, test_df = DatasetManager._load_dataframes(cb_name, dataset_version)
        train_set, test_set, label_categories = DatasetManager._prepare_dataframes(train_df, test_df)

        return DatasetMetadata(codebook_name=cb_name,
                               version=dataset_version,
                               labels=dict(enumerate(label_categories)),
                               num_training_samples=len(train_df),
                               num_test_samples=len(test_df)
                               )

    @staticmethod
    def get_metadata(cb_name: str, dataset_version: str, from_cache: bool = True) -> DatasetMetadata:
        if from_cache:
            return RedisHandler().get_dataset_metadata(cb_name, dataset_version)
        else:
            metadata_file = DataHandler.get_dataset_directory(cb_name, dataset_version, False).joinpath('metadata.json')
            return DatasetMetadata.parse_file(metadata_file)

    @staticmethod
    def is_available(cb_name: str, dataset_version: str, complete_check: bool = False) -> bool:

        try:
            is_in_cache = RedisHandler().get_dataset_metadata(cb_name, dataset_version=dataset_version) is not None
            if complete_check:
                return is_in_cache and DatasetManager._is_valid(cb_name, dataset_version)
            else:
                return is_in_cache
        except DatasetNotAvailableException:
            return False

    @staticmethod
    def _is_valid(cb_name: str, dataset_version: str = "default") -> bool:
        # TODO use feather format
        train_df, test_df = DatasetManager._load_dataframes(cb_name, dataset_version)
        return ("text" and "label" in train_df) and ("text" and "label" in test_df)

    @staticmethod
    def remove(cb_name: str, dataset_version: str):
        try:
            log.info(f"Removing dataset '{dataset_version}' of Codebook {cb_name}")
            RedisHandler().unregister_dataset(cb_name, dataset_version)
            DataHandler.purge_dataset_directory(cb_name=cb_name, dataset_version=dataset_version)
            return True
        except Exception as e:
            return False

    @staticmethod
    def list_datasets(cb_name) -> List[DatasetMetadata]:
        try:
            return RedisHandler().list_datasets(cb_name)
        except Exception as e:
            return []
