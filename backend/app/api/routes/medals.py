import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import col, delete, func, select

from app import crud
from app.api.deps import (
    CurrentUser,
    SessionDep,
    get_current_active_superuser,
)
from app.config.settings import settings
from app.config.security import get_password_hash, verify_password
from app.models import (
    Medal,
    MedalPublic,
    MedalsPublic,
    MedalCreate
)
from app.utils.email import generate_new_account_email, send_email

router = APIRouter(prefix="/medals", tags=["medals"])

@router.post(
    "/", dependencies=[Depends(get_current_active_superuser)], response_model=MedalPublic
)
def create_medal(*, session: SessionDep, medal_in: MedalCreate) -> Any:
    """
    Create new medal.
    """

    user = crud.create_medal(session=session, medal_create=medal_in)
   
    return user

@router.get(
    "/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=MedalsPublic,
)
def read_medals(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve signs.
    """

    count_statement = select(func.count()).select_from(Medal)
    count = session.exec(count_statement).one()

    statement = select(Medal).offset(skip).limit(limit)
    signs = session.exec(statement).all()

    return MedalsPublic(data=signs, count=count)
