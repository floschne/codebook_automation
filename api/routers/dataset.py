from fastapi import APIRouter, Form, UploadFile, File

from api.model import CodebookModel, BooleanResponse, DatasetRequest
from backend.dataset_manager import DatasetManager
from logger import api_logger

PREFIX = "/dataset"
router = APIRouter()


@router.put("/upload/", response_model=BooleanResponse, tags=["dataset"])
async def upload(codebook_name: str = Form(..., description="The name of the Codebook. Case-sensitive!"),
                 codebook_tag_list: str = Form(...,
                                               description="Comma-separated list of tags. E.g. tag1,Tag2 ..."),
                 dataset_version: str = Form(...,
                                             description="Optional version of the dataset. If  not provided "
                                                         "and if there is already an existing dataset with "
                                                         "the same (default) version, the dataset gets "
                                                         "overwritten.  E.g. v1"),
                 dataset_archive: UploadFile = File(..., description="CSV Dataset in a zip-archive.")):
    cbm = CodebookModel(name=codebook_name, tags=codebook_tag_list.replace(" ", "").split(','))
    api_logger.info(f"PUT request on  {PREFIX}/upload/ with Codebook {cbm}")
    dataset_version = "default" if dataset_version is None or dataset_version == "" else dataset_version
    return BooleanResponse(value=DatasetManager.store_archive(cbm, dataset_version, dataset_archive))


@router.post("/available/", response_model=BooleanResponse, tags=["dataset"])
async def is_available(req: DatasetRequest):
    api_logger.info(f"POST request on  {PREFIX}/is_available/ with DatasetRequest {req}")
    return BooleanResponse(value=DatasetManager.is_available(req))


@router.delete("/remove/", response_model=BooleanResponse, tags=["dataset"])
async def remove(req: DatasetRequest):
    api_logger.info(f"DELETE request on  {PREFIX}/remove/ with DatasetRequest {req}")
    return BooleanResponse(value=DatasetManager.remove(req))
