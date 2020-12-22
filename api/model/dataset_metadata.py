from typing import Dict

from pydantic import BaseModel


class DatasetMetadata(BaseModel):
    codebook_name: str
    version: str
    labels: Dict[str, str]
    num_training_samples: int
    num_test_samples: int
