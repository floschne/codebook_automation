from fastapi import APIRouter

from logger import api_logger
from ..model import BooleanResponse

router = APIRouter()


@router.get("/heartbeat", response_model=BooleanResponse, tags=["general"])
async def heartbeat():
    api_logger.info("GET request on /heartbeat")
    return BooleanResponse(value=True)
