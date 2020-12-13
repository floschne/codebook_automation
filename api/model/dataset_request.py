from pydantic import BaseModel

from api.model import CodebookModel


class DatasetRequest(BaseModel):
    cb: CodebookModel
    dataset_version: str
