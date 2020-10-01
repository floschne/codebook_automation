from fastapi import APIRouter

from backend.predictor import Predictor
from logger import api_logger
from ..model import PredictionRequest
from ..model import PredictionResult

PREFIX = "/prediction"
router = APIRouter()

predictor = Predictor()


@router.post("/predict", response_model=PredictionResult, tags=["prediction"])
async def predict(req: PredictionRequest):
    api_logger.info(f"POST request on %s/predict with %s" % (PREFIX, req.json()))
    return predictor.predict(req)
