from fastapi import APIRouter

from logger import api_logger

router = APIRouter()


@router.get("/", response_model=str, tags=["dummy"])
async def hello_world():
    api_logger.info("GET request on /")
    return "Hello world from Codebook Automation API!"
