from fastapi import APIRouter, Form, UploadFile, File

from api.model import CodebookModel, TrainingRequest, TrainingResponse, BooleanResponse
from backend import ModelManager
from backend.training.trainer import Trainer
from logger import api_logger

PREFIX = "/training"
router = APIRouter()

trainer = Trainer()
mm = ModelManager()


@router.put("/upload_dataset/", response_model=BooleanResponse, tags=["training"])
async def upload_dataset(codebook_name: str = Form(..., description="The name of the Codebook. Case-sensitive!"),
                         codebook_tag_list: str = Form(...,
                                                       description="Comma-separated list of tags. E.g. tag1,Tag2 ..."),
                         dataset_version_tag: str = Form(...,
                                                         description="Optional version tag of the dataset. If a tag "
                                                                     "is not provided and if there is already an "
                                                                     "existing dataset with the same (default) tag, "
                                                                     "the dataset gets overwritten.  E.g. v1"),
                         dataset_archive: UploadFile = File(..., description="CSV Dataset in a zip-archive.")):
    cbm = CodebookModel(name=codebook_name, tags=codebook_tag_list.replace(" ", "").split(','))
    api_logger.info(f"POST request on  {PREFIX}/upload_dataset/ with Codebook {cbm}")
    dataset_version_tag = "default" if dataset_version_tag is None or dataset_version_tag == "" else dataset_version_tag
    return BooleanResponse(value=trainer.store_uploaded_dataset(cbm, dataset_version_tag, dataset_archive))


@router.post("/train/", response_model=TrainingResponse, tags=["training"])
async def train(req: TrainingRequest):
    api_logger.info(f"POST request on  {PREFIX}/train/ with TrainingRequest {req}")
    return trainer.train(req)


@router.post("/get_train_log/", tags=["training"])
async def get_train_log(resp: TrainingResponse):
    api_logger.info(f"POST request on  {PREFIX}/get_train_log/ with TrainingResponse {resp}")
    return trainer.get_train_log(resp)
