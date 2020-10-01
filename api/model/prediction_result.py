from typing import Dict

from pydantic import BaseModel


class PredictionResult(BaseModel):
    doc_id: int
    proj_id: int
    codebook_name: str
    predicted_tag: str
    probabilities: Dict[str, float]
