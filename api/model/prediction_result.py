from typing import Dict

from pydantic import BaseModel


class PredictionResult(BaseModel):
    doc_id: int
    proj_id: int
    codebook_name: str
    predicted_tag: str
    probabilities: Dict[str, float]


class MultiDocumentPredictionResult(BaseModel):
    proj_id: int
    codebook_name: str
    predicted_tags: Dict[int, str]  # doc_id -> tag
    probabilities: Dict[int, Dict[str, float]]  # doc_id -> tag -> prob
