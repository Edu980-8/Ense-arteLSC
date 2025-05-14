from typing import List

from sqlmodel import Session, select

from app.models import Category


def get_categories(*, session: Session) -> List[Category]:
    statement = select(Category).order_by(Category.value)
    categories = session.exec(statement)
    return categories.all()