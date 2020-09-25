from typing import List

from pydantic import BaseModel


class Codebook(BaseModel):
    name: str = None
    tags: List[str] = None
