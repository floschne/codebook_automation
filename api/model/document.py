from pydantic import BaseModel


class Document(BaseModel):
    doc_id: int = None
    proj_id: int = None
    text: str = None
