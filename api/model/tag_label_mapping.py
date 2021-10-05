from typing import Dict

from pydantic import BaseModel, Field


class TagLabelMapping(BaseModel):
    cb_name: str = Field(description="The name of the related Codebook")
    version: str = Field(description="The version of the related model", default="default", example="default")
    map: Dict[str, str]
