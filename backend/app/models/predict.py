from typing import TYPE_CHECKING, Optional
import uuid

from sqlmodel import Field, SQLModel, Relationship


from app.models.categories import Category

class PredcitItem():
    sign : str
    probability: float


class PredictBase(SQLModel):
    predict: list[PredcitItem] = Field(
        default_factory=list, description="List of predicted signs with probabilities"
    )

class Predict(PredictBase):
    ...

