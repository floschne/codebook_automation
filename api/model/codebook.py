from typing import List

from pydantic import BaseModel


class Codebook(BaseModel):
    name: int = None
    tags: List[str] = None
