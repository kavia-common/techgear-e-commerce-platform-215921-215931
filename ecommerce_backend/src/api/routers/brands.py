from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from src.db.schemas.catalog import BrandOut, BrandCreate
from src.db.crud.catalog import list_brands, create_brand
from src.db.session import get_db
from src.core.security import admin_required

router = APIRouter(prefix="/brands", tags=["Brands"])


@router.get("/", response_model=List[BrandOut], summary="List brands")
def get_brands(db: Session = Depends(get_db)):
    """
    Return all brands.
    """
    return list_brands(db)


@router.post("/", response_model=BrandOut, dependencies=[Depends(admin_required)], summary="Create brand")
def post_brand(payload: BrandCreate, db: Session = Depends(get_db)):
    """
    Create brand. Admin only.
    """
    return create_brand(db, name=payload.name, description=payload.description)
