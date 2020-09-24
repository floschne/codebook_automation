from pydantic import BaseModel

from .codebook import Codebook
from .document import Document


class PredictionRequest(BaseModel):
    doc: Document
    codebook: Codebook
