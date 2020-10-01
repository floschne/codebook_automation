import json
import os
from typing import Dict, List, Tuple

import tensorflow as tf

from api.model import CodebookModel, DocumentModel, PredictionResult, PredictionRequest, TagLabelMapping
from logger import backend_logger
from .model_manager import ModelManager


class ErroneousModelException(Exception):
    pass


# TODO
#  - split up document text into chunks of MAX_SEQ_LEN (200?!)
#  - Let user select merging strategy of result (i.e. mean, max, min... over all predictions)
#  - check if GPU is available
#  - make this an own process to free GPU Memory https://github.com/tensorflow/tensorflow/issues/19731
#  - documentation
#  - testing


class Predictor(object):
    _singleton = None
    _mm: ModelManager = None

    def __new__(cls, *args, **kwargs):
        if cls._singleton is None:
            # load config file
            config = json.load(open("config.json", "r"))

            # disable GPU for prediction if the configured this way.
            if not bool(config['backend']['use_gpu_for_prediction']):
                backend_logger.info("GPU support for prediction disabled!")
                os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
            else:
                backend_logger.info("GPU support for prediction enabled!")

            backend_logger.info('Instantiating Predictor!')
            cls._singleton = super(Predictor, cls).__new__(cls)
            cls._mm = ModelManager()

        return cls._singleton

    def _load_estimator(self, cb: CodebookModel):
        estimator_path = self._mm.get_model_path(cb)
        estimator = tf.saved_model.load(estimator_path)
        if estimator.signatures["predict"] is None:
            raise ErroneousModelException("Estimator / Model for Codebook %s is erroneous!" % cb.name)

        return estimator

    def predict(self, req: PredictionRequest) -> PredictionResult:
        cb = req.codebook
        doc = req.doc

        # load the estimator # TODO multi proc to free resources after loading
        estimator = self._load_estimator(cb)
        # build the sample(s) for the doc # TODO split doc
        samples = self._build_tf_sample(doc)
        # get predictions # TODO choose pred merge strategy
        pred = estimator.signatures["predict"](examples=samples)

        return self._build_prediction_result(req, pred)

    @staticmethod
    def _build_tf_sample(doc: DocumentModel):
        ex = tf.train.Example()
        ex.features.feature['text'].bytes_list.value.extend([bytes(doc.text, encoding='utf-8')])
        return tf.constant(ex.SerializeToString())

    @staticmethod
    def _build_prediction_result(req: PredictionRequest, pred) -> PredictionResult:

        # parse the prediction
        pred_label = pred['classes'].numpy()[0, 0].decode("utf-8")

        classes = list()
        for c in pred['all_classes'].numpy()[0]:
            if pred['all_classes'].dtype == tf.string:
                classes.append(c.decode("utf-8"))
            else:
                classes.append(c)

        probs = pred['probabilities'].numpy()[0].tolist()

        # apply mapping
        cb = req.codebook
        doc = req.doc
        mapping = req.mapping
        probabilities, pred_tag = Predictor._apply_mapping(pred_label, classes, probs, mapping)

        return PredictionResult(
            doc_id=doc.doc_id,
            proj_id=doc.proj_id,
            codebook_name=cb.name,
            predicted_tag=pred_tag,
            probabilities=probabilities
        )

    @staticmethod
    def _apply_mapping(pred_label: str, classes: List[str], probs: List[float], tag_label_map: TagLabelMapping) \
            -> Tuple[Dict[str, float], str]:

        assert len(probs) == len(classes)
        not_mapped = dict(zip(classes, probs))

        if tag_label_map is not None:
            tag_label_map = tag_label_map.map
            assert len(tag_label_map.keys()) == len(classes)
            label_tag_map = {v: k for k, v in tag_label_map.items()}

            # map the predicted label to tag
            pred_tag = label_tag_map[pred_label]

            # map the other tags
            mapped = dict()
            for m in tag_label_map:
                mapped[m] = not_mapped[tag_label_map[m]]

            return mapped, pred_tag
        else:
            return not_mapped, pred_label
