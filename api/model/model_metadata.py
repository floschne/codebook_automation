from typing import Dict

from pydantic import BaseModel


class ModelMetadata(BaseModel):
    labels: Dict[str, str]
    model_type: str
    embeddings: str = None
    evaluation: Dict[str, float]
    timestamp: str
