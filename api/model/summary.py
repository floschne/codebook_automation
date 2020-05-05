from pydantic import BaseModel


class Summary(BaseModel):
    summary: str
    strategy: str
