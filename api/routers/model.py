from datetime import datetime

from fastapi import APIRouter

from backend.model_manager import ModelManager
from logger import api_logger
from ..model import CodebookModel, BooleanResponse, StringResponse, ModelMetadata

PREFIX = "/model"

router = APIRouter()

mm = ModelManager()


class ModelNotFoundException(Exception):
    def __init__(self, model_id: int = None, codebook_name: str = None):
        self.model_id = model_id,
        self.codebook_name = codebook_name


@router.post("/is_available/", response_model=BooleanResponse, tags=["model"])
async def is_available(cb: CodebookModel):
    api_logger.info(f"POST request on %s/is_available for Codebook %s" % (PREFIX, cb.name))
    return BooleanResponse(value=mm.model_is_available(cb=cb))


@router.put("/init_model/", response_model=StringResponse, tags=["model"])
async def init_model(cb: CodebookModel):
    api_logger.info(f"POST request on %s/init_model for Codebook %s" % (PREFIX, cb.name))
    return StringResponse(value=mm.init_model(cb=cb))


@router.post("/get_metadata/", response_model=ModelMetadata, tags=["model"])
async def get_metadata(cb: CodebookModel):
    api_logger.info(f"POST request on %s/get_metadata/%s" % (PREFIX, cb.name))
    # TODO get info from a DB or check in FS ?!

    model_exists = False
    if not model_exists:
        raise ModelNotFoundException(codebook_name=cb.name, model_id=None)

    return ModelMetadata(model_id=1337,
                         codebook_name=cb.name,
                         labels=["l1", "l2", "l3"],
                         size_mb=500,
                         trained_with_samples=42,
                         last_update=datetime.now())
