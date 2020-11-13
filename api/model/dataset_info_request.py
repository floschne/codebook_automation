from pydantic import BaseModel

from api.model import CodebookModel


class DatasetInfoRequest(BaseModel):
    cb: CodebookModel
    dataset_version_tag: str
