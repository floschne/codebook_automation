import json

import tensorflow as tf

from api.model import CodebookModel, DocumentModel, PredictionResult
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

            backend_logger.info('Instantiating Predictor!')
            cls._singleton = super(Predictor, cls).__new__(cls)
            cls._mm = ModelManager()

        return cls._singleton

    def _load_estimator(self, cb: CodebookModel):
        assert self._mm.model_is_available(cb)

        estimator_path = self._mm.get_model_path(cb)
        estimator = tf.saved_model.load(estimator_path)
        if estimator.signatures["predict"] is None:
            raise ErroneousModelException("Estimator / Model for Codebook %s is erroneous!" % cb.name)

        return estimator

    def predict(self, doc: DocumentModel, cb: CodebookModel) -> PredictionResult:
        # load the estimator # TODO multi proc to free resources after loading
        estimator = self._load_estimator(cb)
        # build the sample(s) for the doc # TODO split doc
        samples = self._build_tf_sample(doc)
        # get predictions # TODO choose pred merge strategy
        pred = estimator.signatures["predict"](examples=samples)

        # TODO create a helper to extract infos and create PredictionResult
        pred_tag = pred['classes'].numpy()[0, 0].decode("utf-8")
        probs = pred['probabilities'].numpy()[0].tolist()

        return PredictionResult(
            doc_id=doc.doc_id,
            proj_id=doc.proj_id,
            codebook_name=cb.name,
            predicted_tag=pred_tag,
            probabilities=probs
        )

    @staticmethod
    def _build_tf_sample(doc: DocumentModel):
        ex = tf.train.Example()
        ex.features.feature['text'].bytes_list.value.extend([bytes(doc.text, encoding='utf-8')])
        return tf.constant(ex.SerializeToString())
