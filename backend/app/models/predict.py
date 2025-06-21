from typing import TYPE_CHECKING, Optional
import uuid

from sqlmodel import Field, SQLModel, Relationship


class PredcitItem(SQLModel):
    label : str
    score: float


class PredictBase(SQLModel):
    predict: list[PredcitItem] = Field(
        default_factory=list, description="List of predicted signs with probabilities"
    )

class Predict(PredictBase):
    ...

