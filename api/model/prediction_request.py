from typing import List, Optional

from pydantic import BaseModel

from .codebook_dto import CodebookDTO
from .document_dto import DocumentDTO
from .tag_label_mapping import TagLabelMapping


class PredictionRequest(BaseModel):
    doc: DocumentDTO
    codebook: CodebookDTO
    mapping: TagLabelMapping = None
    model_version: Optional[str] = "default"


class MultiDocumentPredictionRequest(BaseModel):
    docs: List[DocumentDTO]
    codebook: CodebookDTO
    mapping: Optional[TagLabelMapping] = None
    model_version: Optional[str] = "default"
