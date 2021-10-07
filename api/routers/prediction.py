from fastapi import APIRouter

from api.model import PredictionRequest, MultiDocumentPredictionRequest, PredictionResult, MultiDocumentPredictionResult
from backend import Predictor
from loguru import logger as log

PREFIX = "/prediction"
router = APIRouter()


@router.post("/single", response_model=PredictionResult, tags=["prediction"])
async def predict(req: PredictionRequest):
    log.info(f"POST request on %s/predict with %s" % (PREFIX, req.json()))
    predictor = Predictor()
    return predictor.predict(req)


@router.post("/multiple", response_model=MultiDocumentPredictionResult, tags=["prediction"])
async def predict_multi(req: MultiDocumentPredictionRequest):
    log.info(f"POST request on %s/predict_multi with %s" % (PREFIX, req.json()))
    predictor = Predictor()
    return predictor.predict(req)
