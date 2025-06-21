import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlmodel import col, delete, func, select
from sqlalchemy.orm import selectinload


from app.api.deps import (
    CurrentUser,
    SessionDep,
    get_current_user,
)
from app.config.settings import settings

from app.models.predict import Predict, PredcitItem
from app.services.model_loader import get_model_components
from app.services.predict import infer_video_class

router = APIRouter(prefix="/predict", tags=["predict"])

@router.post(
    "/",
    response_model=Predict,
    dependencies=[Depends(get_current_user)],
)
async def predict(file: UploadFile = File(...)):
    """
    predict a user sign from a video.
    """
    
    try:
        model, processor, id2label = get_model_components(r"app/model_predict")
        results = await infer_video_class(file, model, processor, id2label)
        print(f"Resultados de inferencia: {results}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise e
        raise HTTPException(status_code=500, detail="Error interno de inferencia.")
    return Predict(predict=results)