from typing import List

from fastapi import APIRouter, Depends
from app.crud.categories import get_categories
from app.models import Category
from app.api.deps import SessionDep, get_current_active_superuser



router = APIRouter(tags=["categories"])


@router.get("/",dependencies=[Depends(get_current_active_superuser)],
    response_model=List[Category])
def read_categories(session: SessionDep) -> List[Category]:
    """
    Get all categories
    """
    categories = get_categories(session=session)
    return categories