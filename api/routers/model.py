from typing import Optional

from fastapi import APIRouter, UploadFile, File, Form

from backend import ModelManager
from logger import api_logger
from ..model import BooleanResponse, StringResponse, ModelMetadata

PREFIX = "/model"

router = APIRouter()


@router.post("/available/", response_model=BooleanResponse, tags=["model"])
async def is_available(cb_name: str, model_version: Optional[str] = "default"):
    api_logger.info(
        f"POST request on {PREFIX}/available with model version '{model_version}'for Codebook {cb_name}")
    return BooleanResponse(value=ModelManager.is_available(cb_name=cb_name, model_version=model_version))


@router.post("/metadata/", response_model=ModelMetadata, tags=["model"])
async def get_metadata(cb_name: str, model_version: Optional[str] = "default"):
    api_logger.info(
        f"POST request on {PREFIX}/metadata with model version '{model_version}'for Codebook {cb_name}")
    return ModelManager.get_metadata(cb_name, model_version=model_version)


@router.put("/upload/", response_model=StringResponse, tags=["model"], deprecated=True)
async def upload(codebook_name: str = Form(..., description="The name of the Codebook. Case-sensitive!"),
                 model_version: str = Form(...,
                                           description="Optional version tag of the model. If a tag "
                                                       "is not provided and if there is already an "
                                                       "existing model with the same (default) tag, "
                                                       "the model gets overwritten.  E.g. v1"),
                 model_archive: UploadFile = File(..., description="Zip-archive of the model.")):
    model_version = "default" if model_version is None or model_archive == "" else model_version

    api_logger.info(
        f"PUT request on {PREFIX}/upload with model version '{model_version}'for Codebook {codebook_name}")

    return StringResponse(value=ModelManager.store_uploaded_model(codebook_name, model_version, model_archive))


@router.delete("/remove/", response_model=BooleanResponse, tags=['model'])
async def remove(cb_name: str, model_version: Optional[str] = "default"):
    api_logger.info(
        f"DELETE request on {PREFIX}/remove with model version '{model_version}'for Codebook {cb_name}")
    return BooleanResponse(value=ModelManager.remove(cb_name=cb_name, model_version=model_version))
