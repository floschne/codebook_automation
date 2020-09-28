from datetime import datetime
from typing import List

from pydantic import BaseModel


class ModelMetadata(BaseModel):
    model_id: int
    codebook_name: str
    labels: List[str]
    size_mb: int = None
    trained_with_samples: int = None
    last_update: datetime
