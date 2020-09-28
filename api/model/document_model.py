from pydantic import BaseModel


class DocumentModel(BaseModel):
    doc_id: int = None
    proj_id: int = None
    text: str = None
