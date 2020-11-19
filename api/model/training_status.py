from enum import Enum

from pydantic import BaseModel


class TrainingState(str, Enum):
    preparing: str = "preparing"
    training: str = "training"
    evaluating: str = "evaluating"
    exporting: str = "exporting"
    finished: str = "finished"
    error: str = "error"
    unknown: str = "unknown"


class TrainingStatus(BaseModel):
    state: str = TrainingState.unknown
    process_status: str = "unknown"
