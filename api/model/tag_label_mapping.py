from typing import Dict

from pydantic import BaseModel


class TagLabelMapping(BaseModel):
    map: Dict[str, str]
