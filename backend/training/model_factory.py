from typing import Tuple

import tensorflow as tf
import tensorflow_hub as hub
from loguru import logger as log
from tensorflow_hub.feature_column import DenseFeatureColumn

from api.model import ModelConfig, TrainingRequest
from backend import ModelManager, DataHandler
from backend.exceptions import TFHubEmbeddingException


class ModelFactory(object):
    _singleton = None

    def __new__(cls, *args, **kwargs):
        if cls._singleton is None:
            log.info('Instantiating ModelFactory!')
            cls._singleton = super(ModelFactory, cls).__new__(cls)

        return cls._singleton

    @staticmethod
    def build_model(req: TrainingRequest, n_classes: int) -> \
            Tuple[tf.estimator.DNNClassifier, DenseFeatureColumn, str]:

        # TODO remove if available or other strategy
        model_dir = DataHandler.get_model_directory(req.cb_name, req.model_version, create=True)

        # TODO config in file
        run_config = tf.estimator.RunConfig(model_dir=model_dir,
                                            save_summary_steps=100,
                                            save_checkpoints_steps=500)

        conf = req.model_config
        feature_columns = ModelFactory._create_embedding_feature_column(conf)
        estimator = tf.estimator.DNNClassifier(hidden_units=conf.hidden_units,
                                               feature_columns=feature_columns,
                                               n_classes=n_classes,
                                               dropout=conf.dropout,
                                               optimizer=conf.optimizer,
                                               config=run_config)
        model_id = ModelManager.build_model_id(req.cb_name, req.model_version, req.dataset_version)

        return estimator, feature_columns[0], model_id

    @staticmethod
    def _create_embedding_feature_column(conf: ModelConfig):
        try:
            embedding_column = hub.text_embedding_column_v2(key="text",
                                                            module_path=hub.resolve(conf.embedding_type),
                                                            trainable=False)
            return [embedding_column]
        except Exception as e:
            raise TFHubEmbeddingException(embedding_type=conf.embedding_type)
