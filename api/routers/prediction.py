from fastapi import APIRouter

from api.model import PredictionRequest, MultiDocumentPredictionRequest, PredictionResult, MultiDocumentPredictionResult
from backend import Predictor
from logger import api_logger

PREFIX = "/prediction"
router = APIRouter()


@router.post("/single", response_model=PredictionResult, tags=["prediction"], deprecated=True)
async def predict(req: PredictionRequest):
    api_logger.info(f"POST request on %s/predict with %s" % (PREFIX, req.json()))
    predictor = Predictor()
    return predictor.predict(req)


@router.post("/multiple", response_model=MultiDocumentPredictionResult, tags=["prediction"])
async def predict_multi(req: MultiDocumentPredictionRequest):
    api_logger.info(f"POST request on %s/predict_multi with %s" % (PREFIX, req.json()))
    predictor = Predictor()
    return predictor.predict(req)
