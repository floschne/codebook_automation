from pydantic import BaseModel

from .codebook_model import CodebookModel
from .document_model import DocumentModel


class PredictionRequest(BaseModel):
    doc: DocumentModel
    codebook: CodebookModel
