from pydantic import BaseModel

from .codebook_model import CodebookModel
from .document_model import DocumentModel
from .tag_label_mapping import TagLabelMapping


class PredictionRequest(BaseModel):
    doc: DocumentModel
    codebook: CodebookModel
    mapping: TagLabelMapping = None
