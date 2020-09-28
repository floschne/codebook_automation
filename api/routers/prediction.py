from fastapi import APIRouter

from logger import api_logger
from ..model import PredictionRequest
from ..model import PredictionResult

PREFIX = "/prediction"
router = APIRouter()


@router.post("/predict", response_model=PredictionResult, tags=["prediction"])
async def predict(req: PredictionRequest):
    api_logger.info(f"POST request on %s/predict with %s" % (PREFIX, req.json()))
    return PredictionResult(doc_id=req.doc.doc_id,
                            proj_id=req.doc.proj_id,
                            codebook_name=req.codebook.name,
                            predicted_tag=req.codebook.tags[-1])
