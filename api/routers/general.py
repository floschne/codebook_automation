from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from api.model import BooleanResponse
from logger import api_logger

router = APIRouter()


@router.get("/heartbeat", response_model=BooleanResponse, tags=["general"])
async def heartbeat():
    api_logger.info("GET request on /heartbeat")
    return BooleanResponse(value=True)


@router.get("/", tags=["general"], description="Redirection to /docs")
async def root_to_docs():
    api_logger.info("GET request on / -> redirecting to /docs")
    return RedirectResponse("/docs")
