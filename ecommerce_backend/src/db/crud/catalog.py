from sqlalchemy.orm import Session
from typing import List
from src.db.models.catalog import Category, Brand, Product


# PUBLIC_INTERFACE
def list_categories(db: Session) -> List[Category]:
    """List all categories."""
    return db.query(Category).order_by(Category.name).all()


# PUBLIC_INTERFACE
def create_category(db: Session, name: str, description: str | None = None) -> Category:
    """Create a category."""
    category = Category(name=name, description=description)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


# PUBLIC_INTERFACE
def list_brands(db: Session) -> List[Brand]:
    """List all brands."""
    return db.query(Brand).order_by(Brand.name).all()


# PUBLIC_INTERFACE
def create_brand(db: Session, name: str, description: str | None = None) -> Brand:
    """Create a brand."""
    brand = Brand(name=name, description=description)
    db.add(brand)
    db.commit()
    db.refresh(brand)
    return brand


# PUBLIC_INTERFACE
def list_products(db: Session) -> List[Product]:
    """List all products."""
    return db.query(Product).order_by(Product.id.desc()).all()


# PUBLIC_INTERFACE
def create_product(
    db: Session,
    name: str,
    description: str | None,
    price_cents: int,
    currency: str,
    stock: int,
    image_url: str | None,
    category_id: int | None,
    brand_id: int | None,
) -> Product:
    """Create a product."""
    product = Product(
        name=name,
        description=description,
        price_cents=price_cents,
        currency=currency,
        stock=stock,
        image_url=image_url,
        category_id=category_id,
        brand_id=brand_id,
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product
