from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from loguru import logger as log

from api.model import BooleanResponse

router = APIRouter()


@router.get("/heartbeat", response_model=BooleanResponse, tags=["general"])
async def heartbeat():
    log.info("GET request on /heartbeat")
    return BooleanResponse(value=True)


@router.get("/", tags=["general"], description="Redirection to /docs")
async def root_to_docs():
    log.info("GET request on / -> redirecting to /docs")
    return RedirectResponse("/docs")
