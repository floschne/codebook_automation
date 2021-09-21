from typing import List

from fastapi import APIRouter, Form, UploadFile, File
from loguru import logger as log

from api.model import BooleanResponse, DatasetMetadata
from backend.dataset_manager import DatasetManager

PREFIX = "/dataset"
router = APIRouter()


@router.put("/upload/", response_model=DatasetMetadata, tags=["dataset"])
async def upload(cb_name: str = Form(..., description="The name of the Codebook. Case-sensitive!"),
                 dataset_version: str = Form(...,
                                             description="Optional version of the dataset. If  not provided "
                                                         "and if there is already an existing dataset with "
                                                         "the same (default) version, the dataset gets "
                                                         "overwritten.  E.g. v1"),
                 dataset_archive: UploadFile = File(..., description="CSV Dataset in a zip-archive.")):
    log.info(f"PUT request on  {PREFIX}/upload/ with Codebook {cb_name}")
    dataset_version = "default" if dataset_version is None or dataset_version == "" else dataset_version
    return DatasetManager.store_archive(cb_name, dataset_version, dataset_archive)


@router.get("/available/", response_model=BooleanResponse, tags=["dataset"])
async def is_available(cb_name: str, dataset_version: str):
    log.info(f"POST request on  {PREFIX}/available/ with model version '{dataset_version}'for Codebook {cb_name}")
    return BooleanResponse(value=DatasetManager.is_available(cb_name, dataset_version))


@router.get("/list/", response_model=List[DatasetMetadata], tags=["dataset"])
async def list_datasets(cb_name: str):
    log.info(f"POST request on  {PREFIX}/list/ with Codebook Name {cb_name}")
    return DatasetManager.list_datasets(cb_name)


@router.get("/metadata/", response_model=DatasetMetadata, tags=["dataset"])
async def get_metadata(cb_name: str, dataset_version: str):
    log.info(f"POST request on  {PREFIX}/metadata/ with model version '{dataset_version}'for Codebook {cb_name}")
    return DatasetManager.get_metadata(cb_name, dataset_version)


@router.delete("/remove/", response_model=BooleanResponse, tags=["dataset"])
async def remove(cb_name: str, dataset_version: str):
    log.info(f"DELETE request on  {PREFIX}/remove/ with model version '{dataset_version}'for Codebook {cb_name}")
    return BooleanResponse(value=DatasetManager.remove(cb_name, dataset_version))
