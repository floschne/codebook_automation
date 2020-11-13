from enum import Enum

from pydantic import BaseModel


class TrainingState(str, Enum):
    training: str = "training"
    evaluate: str = "evaluate"
    exported: str = "exported"
    error: str = "error"
    unknown: str = "unknown"


class TrainingStatus(BaseModel):
    state: str
    process_alive: bool = False
