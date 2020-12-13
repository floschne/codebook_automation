from typing import Union, Tuple, List

import numpy as np
import pandas as pd
import tensorflow as tf
from fastapi import UploadFile

from api.model import CodebookModel, DatasetRequest
from logger import backend_logger
from .data_handler import DataHandler
from .exceptions import ErroneousDatasetException, DatasetNotAvailableException


class DatasetManager(object):
    _singleton = None

    def __new__(cls, *args, **kwargs):
        if cls._singleton is None:
            backend_logger.info('Instantiating DatasetManager!')
            cls._singleton = super(DatasetManager, cls).__new__(cls)
        return cls._singleton

    @staticmethod
    def store_archive(cb: CodebookModel, dataset_version: str, dataset_archive: UploadFile) -> bool:
        backend_logger.info(f"Successfully received dataset archive for Codebook {cb.name}")

        try:
            path = DataHandler.store_dataset(cb=cb, dataset_archive=dataset_archive, dataset_version=dataset_version)
        except Exception as e:
            raise ErroneousDatasetException(dataset_version, cb,
                                            f"Error while persisting dataset for Codebook {cb.name}!", caused_by=str(e))

        if not DatasetManager._is_valid(cb, dataset_version=dataset_version):
            raise ErroneousDatasetException(dataset_version, cb,
                                            f"Error while persisting dataset for Codebook {cb.name} under {str(path)}")
        backend_logger.info(
            f"Successfully persisted dataset '{dataset_version}' for Codebook <{cb.name}> under {str(path)}")
        return True

    @staticmethod
    def get_tensorflow_dataset(cb: CodebookModel, dataset_version: str = "default", get_labels_only=False) -> \
            Union[List[str], Tuple[tf.data.Dataset, tf.data.Dataset, List[str]]]:

        # load and prepare the dataframes
        train_df, test_df = DatasetManager._load_dataframes(cb, dataset_version)
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
    def _load_dataframes(cb: CodebookModel, dataset_version: str = "default") -> Tuple[pd.DataFrame, pd.DataFrame]:
        dataset_dir = DataHandler.get_dataset_directory(cb, dataset_version=dataset_version)

        # make sure train.csv & test.csv is available and has two columns 'text' & 'label'
        train_csv = dataset_dir.joinpath("train.csv")
        test_csv = dataset_dir.joinpath("test.csv")

        if not train_csv.exists() or not test_csv.exists():
            raise DatasetNotAvailableException(cb=cb, dataset_version=dataset_version)
        else:
            # TODO
            #  - this might be very inefficient for large datasets?!
            #  - use chunks for large datasets
            train_df = pd.read_csv(train_csv)
            test_df = pd.read_csv(test_csv)
            return train_df, test_df

    @staticmethod
    def is_available(req: DatasetRequest) -> bool:
        # TODO just ask redis is available w/o checking validity (maybe use flag to do so)
        try:
            return DatasetManager._is_valid(req.cb, req.dataset_version)
        except DatasetNotAvailableException:
            return False

    @staticmethod
    def _is_valid(cb: CodebookModel, dataset_version: str = "default") -> bool:
        train_df, test_df = DatasetManager._load_dataframes(cb, dataset_version)
        return ("text" and "label" in train_df) and ("text" and "label" in test_df)

    @staticmethod
    def remove(req: DatasetRequest):
        # TODO unregister
        try:
            cb = req.cb
            dataset_version = req.dataset_version
            backend_logger.info(f"Removing dataset '{dataset_version}' of Codebook {cb.name}")
            DataHandler.purge_dataset_directory(cb=cb, dataset_version=dataset_version)
            return True
        except Exception as e:
            return False
