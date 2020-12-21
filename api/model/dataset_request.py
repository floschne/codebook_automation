from pydantic import BaseModel


class DatasetRequest(BaseModel):
    cb_name: str
    dataset_version: str
