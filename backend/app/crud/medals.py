from sqlmodel import Session

from app.models import Medal, MedalCreate


def create_medal(*, session: Session, medal_create: MedalCreate) -> Medal:
    db_obj = Medal.model_validate(medal_create)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj
