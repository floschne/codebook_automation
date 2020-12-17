from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from api.model import TrainingRequest, TrainingResponse, TrainingStatus, \
    TrainingState
from backend.training.trainer import Trainer
from logger import api_logger

PREFIX = "/training"
router = APIRouter()


@router.post("/train/", response_model=TrainingResponse, tags=["training"])
async def train(req: TrainingRequest):
    api_logger.info(f"POST request on  {PREFIX}/train/ with TrainingRequest {req}")
    return Trainer.train(req)


@router.post("/log/", tags=["training"])
async def get_train_log(resp: TrainingResponse):
    api_logger.info(f"POST request on  {PREFIX}/get_train_log/ with TrainingResponse {resp}")
    log_path = Trainer.get_training_log(resp)
    file_like = open(str(log_path), mode="rb")
    return StreamingResponse(file_like, media_type="text/plain")


@router.post("/status/", response_model=TrainingStatus, tags=["training"])
async def get_training_status(resp: TrainingResponse):
    api_logger.info(f"POST request on  {PREFIX}/get_training_status/ with TrainingResponse {resp}")
    status = Trainer.get_train_status(resp)
    if status is None:
        return TrainingStatus(state=TrainingState.finished, process_status="finished")
    else:
        return status
