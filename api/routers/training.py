from fastapi import APIRouter, Form, UploadFile, File

from api.model import StringResponse, CodebookModel
from backend import ModelManager
from backend.trainer import Trainer
from logger import api_logger

PREFIX = "/training"
router = APIRouter()

trainer = Trainer()
mm = ModelManager()


@router.put("/upload_dataset/", response_model=StringResponse, tags=["training"])
async def upload_dataset(codebook_name: str = Form(..., description="The name of the Codebook. Case-sensitive!"),
                         codebook_tag_list: str = Form(...,
                                                       description="Comma-separated list of tags. E.g. tag1,Tag2 ..."),
                         dataset_version_tag: str = Form(...,
                                                         description="Optional version tag of the dataset. If a tag "
                                                                     "is not provided and if there is already an "
                                                                     "existing dataset with the same (default) tag, "
                                                                     "the dataset gets overwritten.  E.g. v1"),
                         dataset_archive: UploadFile = File(..., description="CSV Dataset in a zip-archive.")):
    api_logger.info(f"POST request on %s/upload_dataset/ with Codebook %s" % (PREFIX, codebook_name))
    cbm = CodebookModel(name=codebook_name, tags=codebook_tag_list.replace(" ", "").split(','))
    dataset_version_tag = "default" if dataset_version_tag is None or dataset_version_tag == "" else dataset_version_tag
    return StringResponse(value=str(trainer.store_uploaded_dataset(cbm, dataset_version_tag, dataset_archive)))
