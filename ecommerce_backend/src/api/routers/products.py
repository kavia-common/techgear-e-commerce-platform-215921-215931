from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from src.db.schemas.catalog import ProductOut, ProductCreate
from src.db.crud.catalog import list_products, create_product
from src.db.session import get_db
from src.core.security import admin_required

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/", response_model=List[ProductOut], summary="List products")
def get_products(db: Session = Depends(get_db)):
    """
    Return all products (seeded for dev).
    """
    return list_products(db)


@router.post("/", response_model=ProductOut, dependencies=[Depends(admin_required)], summary="Create product")
def post_product(payload: ProductCreate, db: Session = Depends(get_db)):
    """
    Create a new product. Admin only.
    """
    return create_product(
        db,
        name=payload.name,
        description=payload.description,
        price_cents=payload.price_cents,
        currency=payload.currency,
        stock=payload.stock,
        image_url=payload.image_url,
        category_id=payload.category_id,
        brand_id=payload.brand_id,
    )
