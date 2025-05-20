import uuid
from typing import Any

from fastapi import APIRouter, Depends
from sqlmodel import func, select

from app import crud
from app.api.deps import (
    CurrentUser,
    SessionDep,
    get_current_active_superuser,
)
from app.models import (
    Medal,
    MedalPublic,
    MedalsPublic,
    MedalCreate
)

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
    "/by-user/{user_id}",
    response_model=MedalsPublic,
    dependencies=[Depends(get_current_active_superuser)],
)
def get_medals_by_user(*, session: SessionDep, user_id: uuid.UUID) -> Any:
    """
    Retrieve all medals for a specific user.
    """
    statement = select(Medal).where(Medal.user_id == user_id)
    medals = session.exec(statement).all()
    count = len(medals)
    return MedalsPublic(data=medals, count=count)


