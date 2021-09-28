from fastapi import APIRouter
from loguru import logger as log

from api.model import TagLabelMapping
from backend import RedisHandler
from backend.exceptions import TagLabelMappingNotAvailableException

PREFIX = "/mapping"
router = APIRouter()


@router.put("/register/", tags=["mapping"])
async def register(mapping: TagLabelMapping):
    log.info(f"PUT request on {PREFIX}/register")
    RedisHandler().register_mapping(mapping.cb_name, mapping)


@router.get("/get/", response_model=TagLabelMapping, tags=["mapping"])
async def get(cb_name: str, model_version: str):
    log.info(f"GET request on {PREFIX}/get")
    return RedisHandler().get_mapping(cb_name, model_version)


@router.delete("/unregister/", tags=["mapping"])
async def unregister(cb_name: str, model_version: str):
    log.info(f"DELETE request on {PREFIX}/remove")
    RedisHandler().unregister_mapping(cb_name, model_version)


@router.post("/update/", tags=["mapping"])
async def update(cb_name: str, mapping: TagLabelMapping):
    log.info(f"POST request on {PREFIX}/update")
    try:
        # if a mapping is not yet registered it cannot be unregistered and an exception is thrown. this is ignored here
        RedisHandler().unregister_mapping(cb_name, mapping.version)
    except TagLabelMappingNotAvailableException as e:
        pass
    RedisHandler().register_mapping(cb_name, mapping)
