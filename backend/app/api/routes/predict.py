import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlmodel import col, delete, func, select
from sqlalchemy.orm import selectinload

from app import crud
from app.api.deps import (
    CurrentUser,
    SessionDep,
    get_current_user,
)
from app.models import (
    Sign,
    SignPublic,
    SignsPublic
)
from app.models import Predict, PredcitItem

router = APIRouter(prefix="/predict", tags=["predict"])

router.post(
    "/",
    response_model=Predict,
    dependencies=[Depends(get_current_user)],
)
async def predict(file: UploadFile = File(...)):
    """
    predict a user sign from a video.
    """
    p1 = PredcitItem(
        sign="example_sign",
        probability=0.95
    )
    p2 = PredcitItem(
        sign="another_sign",
        probability=0.85
    )
    predict = Predict(predict=[p1, p2])
    return predict