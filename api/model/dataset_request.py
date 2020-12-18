from pydantic import BaseModel

from api.model import CodebookDTO


class DatasetRequest(BaseModel):
    cb: CodebookDTO
    dataset_version: str
