from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from src.db.schemas.catalog import ProductOut, ProductCreate
from src.db.schemas.common import Message
from src.db.session import get_db
from src.core.security import admin_required
from src.db.models.catalog import Product
from src.db.crud.catalog import create_product

router = APIRouter(prefix="/products", tags=["Products"])


class PaginatedProducts(Message):
    """Paginated product response with metadata."""
    items: List[ProductOut] = []
    total: int = 0
    page: int = 1
    size: int = 10


@router.get(
    "/",
    response_model=PaginatedProducts,
    summary="List products",
)
def get_products(
    db: Session = Depends(get_db),
    # Filters
    q: Optional[str] = Query(None, description="Search term for product name/description"),
    category_id: Optional[int] = Query(None, description="Filter by category id"),
    brand_id: Optional[int] = Query(None, description="Filter by brand id"),
    min_price: Optional[int] = Query(None, description="Minimum price in cents"),
    max_price: Optional[int] = Query(None, description="Maximum price in cents"),
    in_stock: Optional[bool] = Query(None, description="Only products with stock > 0"),
    # Sorting
    sort: Optional[str] = Query("created_at:desc", description="Sort field and direction, e.g., price_cents:asc"),
    # Pagination
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Page size"),
):
    """
    Return products with optional filtering, sorting, and pagination.
    Supported sort fields: id, created_at, price_cents, name, stock. Use ':asc' or ':desc'.
    """
    query = db.query(Product)

    # Filters
    if q:
        like = f"%{q}%"
        query = query.filter((Product.name.ilike(like)) | (Product.description.ilike(like)))
    if category_id:
        query = query.filter(Product.category_id == category_id)
    if brand_id:
        query = query.filter(Product.brand_id == brand_id)
    if min_price is not None:
        query = query.filter(Product.price_cents >= min_price)
    if max_price is not None:
        query = query.filter(Product.price_cents <= max_price)
    if in_stock is True:
        query = query.filter(Product.stock > 0)
    elif in_stock is False:
        query = query.filter(Product.stock <= 0)

    total = query.count()

    # Sorting
    sort_field = "created_at"
    sort_dir = "desc"
    if sort and ":" in sort:
        sort_field, sort_dir = sort.split(":", 1)
    elif sort:
        sort_field = sort

    sortable = {
        "id": Product.id,
        "created_at": Product.created_at,
        "price_cents": Product.price_cents,
        "name": Product.name,
        "stock": Product.stock,
    }
    col = sortable.get(sort_field, Product.created_at)
    if sort_dir.lower() == "asc":
        query = query.order_by(col.asc())
    else:
        query = query.order_by(col.desc())

    # Pagination
    items = query.offset((page - 1) * size).limit(size).all()
    return PaginatedProducts(message="OK", items=items, total=total, page=page, size=size)


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
