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
    Sign,
    SignPublic,
    SignsPublic
)
from app.utils.email import generate_new_account_email, send_email

router = APIRouter(prefix="/signs", tags=["signs"])


@router.get(
    "/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=SignsPublic,
)
def read_signs(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve signs.
    """

    count_statement = select(func.count()).select_from(Sign)
    count = session.exec(count_statement).one()

    statement = select(Sign).offset(skip).limit(limit)
    signs = session.exec(statement).all()

    return SignsPublic(data=signs, count=count)
