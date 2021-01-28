from typing import Dict, Any

from pydantic import BaseModel


class ModelMetadata(BaseModel):
    codebook_name: str
    version: str
    dataset_version: str
    labels: Dict[str, str]
    model_type: str
    evaluation: Dict[str, float]
    model_config: Dict[Any, Any]
