from fastapi import APIRouter

from api.model import PredictionRequest
from api.model.prediction_result import PredictionResult
from logger import api_logger

router = APIRouter()


@router.get("/", tags=["dummy"])
async def get_root():
    api_logger.info("GET request on /")
    return "Hello world from Codebook Automation API!"


@router.post("/predict", response_model=PredictionResult, tags=["dummy"])
async def get_info(req: PredictionRequest):
    api_logger.info(f"POST request on /predict with %s" % req.json())
    return PredictionResult(doc_id=req.doc.doc_id,
                            proj_id=req.doc.proj_id,
                            codebook_name=req.codebook.name,
                            predicted_tag=req.codebook.tags[0])
