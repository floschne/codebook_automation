from enum import Enum
from typing import List

from pydantic import BaseModel, Field


class OptimizerIdentifier(str, Enum):
    """
     Possible tf.optimizer
     check out https://www.tensorflow.org/api_docs/python/tf/keras/optimizers for details!
    """
    adam: str = "Adam"
    sgd: str = "SGD"
    adagrad: str = "Adagrad"
    rmsprop: str = "RMSProp"
    ftrl: str = "Ftrl"


class ActivationFunctionIdentifier(str, Enum):
    """
    Possible activation functions
    """
    relu: str = "relu"
    sigmoid: str = "sigmoid"
    tanh: str = "tanh"
    exponential: str = "exponential"


class ModelConfig(BaseModel):
    embedding_type: str = Field(default="https://tfhub.dev/google/universal-sentence-encoder/2",
                                example="https://tfhub.dev/google/universal-sentence-encoder/2")
    hidden_units: List[int] = Field(default=[1024, 1024, 512, 64], example=[1024, 1024, 512, 64])
    dropout: float = Field(default=0.2, example=0.2)
    optimizer: OptimizerIdentifier = "Adam"
    early_stopping: bool = Field(default=False, example=False)
    activation_fn: ActivationFunctionIdentifier = "relu"
