from pydantic import BaseModel, Field

from .model_config import ModelConfig


class TrainingRequest(BaseModel):
    cb_name: str = Field(description="The name of the Codebook for which the model gets trained!")
    model_config: ModelConfig
    model_version: str = Field(default="default", example="default")
    dataset_version: str = Field(default="default", example="default")
    batch_size_train: int = Field(default=32, example=32)
    batch_size_test: int = Field(default=32, example=32)
    max_steps_train: int = Field(default=100, example=10000)
    max_steps_test: int = Field(default=100, example=1000)
