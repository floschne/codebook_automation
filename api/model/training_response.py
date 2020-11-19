from pydantic import BaseModel, Field


class TrainingResponse(BaseModel):
    """
    id for a training to check if its done or not (or even progress), get log etc
    """
    model_id: str = Field(description="Use this ID to get info about the status of the model!")
