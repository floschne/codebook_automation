from pydantic import BaseModel

from api.model import Codebook, Document


class PredictionRequest(BaseModel):
    doc: Document
    codebook: Codebook
