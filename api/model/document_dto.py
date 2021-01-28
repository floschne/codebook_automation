from pydantic import BaseModel


class DocumentDTO(BaseModel):
    doc_id: int = None
    proj_id: int = None
    text: str = None
