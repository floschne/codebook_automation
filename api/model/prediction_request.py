from typing import List, Optional

from pydantic import BaseModel

from .codebook_model import CodebookModel
from .document_model import DocumentModel
from .tag_label_mapping import TagLabelMapping


class PredictionRequest(BaseModel):
    doc: DocumentModel
    codebook: CodebookModel
    mapping: TagLabelMapping = None
    model_version: Optional[str] = "default"


class MultiDocumentPredictionRequest(BaseModel):
    docs: List[DocumentModel]
    codebook: CodebookModel
    mapping: Optional[TagLabelMapping] = None
    model_version: Optional[str] = "default"
