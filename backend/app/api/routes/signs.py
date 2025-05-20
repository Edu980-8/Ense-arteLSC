import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import col, delete, func, select
from sqlalchemy.orm import selectinload

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
from app.models.user_signs import UserSign, UserSignCreate
from app.utils.email import generate_new_account_email, send_email

router = APIRouter(prefix="/signs", tags=["signs"])


@router.get(
    "/",
    # dependencies=[Depends(get_current_active_superuser)],
    response_model=SignsPublic,
)
def read_signs(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve signs.
    """

    count_statement = select(func.count()).select_from(Sign)
    count = session.exec(count_statement).one()

    statement = (
        select(Sign)
        .options(selectinload(Sign.category))  # <-- Esto carga la relación
        .offset(skip)
        .limit(limit)
    )
    signs = session.exec(statement).all()

    return SignsPublic(data=signs, count=count)

@router.get(
    "/by-user/{user_id}",
    response_model=SignsPublic,
    dependencies=[Depends(get_current_active_superuser)],
)
def get_signs_by_user(*, session: SessionDep, user_id: uuid.UUID) -> Any:
    """
    Retrieve all signs associated with a specific user.
    """
    # Obtener los registros intermedios de UserSign
    user_signs = session.exec(
        select(UserSign).where(UserSign.user_id == user_id)
    ).all()

    # Extraer IDs de las señas
    sign_ids = [us.sign_id for us in user_signs]

    # Obtener las señas correspondientes
    signs = session.exec(
        select(Sign).where(Sign.id.in_(sign_ids))
    ).all()

    return SignsPublic(data=signs, count=len(signs))

@router.post(
    "/assign-to-user",
    response_model=UserSignCreate,
    dependencies=[Depends(get_current_active_superuser)],
)
def assign_sign_to_user(*, session: SessionDep, user_sign_in: UserSignCreate) -> Any:
    """
    Assign a sign to a user.
    """
    # Verificar si ya existe esa relación
    existing = session.exec(
        select(UserSign).where(
            (UserSign.user_id == user_sign_in.user_id) &
            (UserSign.sign_id == user_sign_in.sign_id)
        )
    ).first()

    if existing:
        return existing  # o lanzar error si no deseas duplicados

    user_sign = UserSign(**user_sign_in.model_dump())
    session.add(user_sign)
    session.commit()
    session.refresh(user_sign)
    return user_sign