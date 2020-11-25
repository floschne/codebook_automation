from typing import Dict, Any

from pydantic import BaseModel


class ModelMetadata(BaseModel):
    labels: Dict[str, str]
    model_type: str
    evaluation: Dict[str, float]
    model_config: Dict[Any, Any]
    timestamp: str
