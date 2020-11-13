import re
from pathlib import Path
from typing import Union, Tuple, List

import numpy as np
import pandas as pd
import tensorflow as tf
import tensorflow_hub as hub
from tensorflow_hub.feature_column import DenseFeatureColumn

from api.model import CodebookModel, ModelConfig, TrainingRequest
from logger import backend_logger
from ..data_handler import DataHandler
from ..exceptions import InvalidModelIdException, DatasetNotAvailableException, TFHubEmbeddingException
from ..model_manager import ModelManager


class ModelFactory(object):
    _singleton = None

    def __new__(cls, *args, **kwargs):
        if cls._singleton is None:
            backend_logger.info('Instantiating ModelFactory!')

            cls._singleton = super(ModelFactory, cls).__new__(cls)
            cls._dh = DataHandler()
            cls._mm = ModelManager()

        return cls._singleton

    def create_datasets(self, cb: CodebookModel, dataset_version: str = "default", get_labels_only=False) -> \
            Union[List[str], Tuple[tf.data.Dataset, tf.data.Dataset, List[str]]]:
        train_df, test_df = self.dataset_is_available(cb, dataset_version, return_dataframes=True)
        if train_df is None or test_df is None:
            raise DatasetNotAvailableException(dataset_version=dataset_version, cb=cb)

        # prepare the dataframes
        train_set, test_set, label_categories = self._prepare_dataframes(train_df, test_df)
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

    def dataset_is_available(self, cb: CodebookModel, dataset_version: str, return_dataframes=False) -> \
            Union[bool, Tuple[pd.DataFrame, pd.DataFrame]]:

        dataset_dir = self._dh.get_dataset_directory(cb, dataset_version=dataset_version)
        # make sure train.csv & test.csv is available and has two columns 'text' & 'label'
        train_csv = dataset_dir.joinpath("train.csv")
        test_csv = dataset_dir.joinpath("test.csv")

        if not train_csv.exists() and not test_csv.exists():
            return False
        else:
            # TODO this might be very inefficient for large datasets?!
            train_df = pd.read_csv(train_csv)
            test_df = pd.read_csv(test_csv)
            if (not ("text" and "label" in train_df)) or (not ("text" and "label" in test_df)):
                return False
            else:
                if return_dataframes:
                    return train_df, test_df

        return True

    def build_model(self, req: TrainingRequest, n_classes: int) -> \
            Tuple[tf.estimator.DNNClassifier, DenseFeatureColumn, str]:

        # TODO remove if available or other strategy
        model_dir = self._dh.get_model_directory(req.cb, req.model_version, create=True)

        # TODO config in file
        run_config = tf.estimator.RunConfig(model_dir=model_dir,
                                            save_summary_steps=100,
                                            save_checkpoints_steps=500)

        conf = req.model_config
        feature_columns = self._create_embedding_feature_column(conf)
        estimator = tf.estimator.DNNClassifier(hidden_units=conf.hidden_units,
                                               feature_columns=feature_columns,
                                               n_classes=n_classes,
                                               dropout=conf.dropout,
                                               optimizer=conf.optimizer,
                                               config=run_config)
        model_id = self.get_model_id(req)

        return estimator, feature_columns[0], model_id

    def get_model_id(self, req: TrainingRequest) -> str:
        # TODO make this more stable
        return self._dh.get_data_handle(cb=req.cb) + "_m_" + req.model_version + "_d_" + req.dataset_version

    def get_model_dir(self, model_id: str, create: bool = False) -> Path:
        model_info = self._validate_model_id(model_id)
        return self._dh.get_model_dir_from_handle(cb_data_handle=model_info['cb_data_handle'],
                                                  model_version=model_info['model_version'],
                                                  create=create)

    def get_log_file(self, model_id: str, create: bool = True) -> Path:
        model_dir = self.get_model_dir(model_id=model_id, create=create)
        log_path = model_dir.joinpath("model.log")
        if create:
            log_path.touch()
        # TODO throw exception
        assert log_path.exists(), f"Log File not found at {log_path}"
        return log_path

    def get_metadata_file(self, model_id: str) -> Path:
        model_dir = self.get_model_dir(model_id=model_id)
        metadata_path = model_dir.joinpath("metadata.json")
        return metadata_path

    @staticmethod
    def _prepare_dataframes(train_set: pd.DataFrame, test_set: pd.DataFrame) -> (pd.DataFrame, pd.DataFrame):
        # convert to str
        train_set['text'] = train_set['text'].astype(str)
        test_set['text'] = train_set['text'].astype(str)
        train_set['label'] = train_set['label'].astype(str)
        test_set['label'] = train_set['label'].astype(str)

        # convert to categorical data
        # TODO maybe outsource label dict to file in dataset archive
        # FIXME in very rare situations induced by the dataset designer,
        #  train_set could not contain all labels from test_set or vice versa...)
        train_cats = pd.Categorical(train_set['label'])
        test_cats = pd.Categorical(test_set['label'])
        # make sure labels are int32
        train_set['label'] = np.asarray(train_cats.codes, dtype=np.int32)
        test_set['label'] = np.asarray(test_cats.codes, dtype=np.int32)

        return train_set, test_set, list(train_cats.categories)

    @staticmethod
    def _create_embedding_feature_column(conf: ModelConfig):
        try:
            embedding_column = hub.text_embedding_column(key="text",
                                                         module_spec=conf.embedding_type,
                                                         trainable=False)
            return [embedding_column]
        except Exception as e:
            raise TFHubEmbeddingException(embedding_type=conf.embedding_type)

    @staticmethod
    def _validate_model_id(model_id: str):
        model_id_pattern = re.compile(r"[a-f0-9]{32}_m_[a-z0-9]+_d_[a-z0-9]+")
        if not model_id_pattern.match(model_id):
            raise InvalidModelIdException(model_id)
        else:
            data = model_id.split("_")
            return {
                'cb_data_handle': data[0],
                'model_version': data[2],
                'dataset_version': data[4]
            }
