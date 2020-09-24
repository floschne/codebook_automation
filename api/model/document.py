from pydantic import BaseModel


class Document(BaseModel):
    doc_id: int = None
    proj_id: str = None
    text: str = None
