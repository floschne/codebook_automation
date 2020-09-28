from typing import List

from pydantic import BaseModel


class CodebookModel(BaseModel):
    name: str
    tags: List[str]
