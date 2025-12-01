from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from src.db.schemas.catalog import CategoryOut, CategoryCreate
from src.db.crud.catalog import list_categories, create_category
from src.db.session import get_db
from src.core.security import admin_required

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/", response_model=List[CategoryOut], summary="List categories")
def get_categories(db: Session = Depends(get_db)):
    """
    Return all categories.
    """
    return list_categories(db)


@router.post("/", response_model=CategoryOut, dependencies=[Depends(admin_required)], summary="Create category")
def post_category(payload: CategoryCreate, db: Session = Depends(get_db)):
    """
    Create category. Admin only.
    """
    return create_category(db, name=payload.name, description=payload.description)
