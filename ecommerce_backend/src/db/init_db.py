from sqlalchemy.orm import Session
from src.db.crud.catalog import create_brand, create_category, create_product
from src.db.crud.user import create_user, get_user_by_email
from src.core.security import get_password_hash


def seed(db: Session) -> None:
    """Populate development database with sample data if not present."""
    # Admin user
    admin_email = "admin@techgear.local"
    if not get_user_by_email(db, admin_email):
        create_user(
            db,
            email=admin_email,
            hashed_password=get_password_hash("admin123"),
            full_name="Admin",
            is_admin=True,
        )

    # Categories
    laptops = create_category(db, name="Laptops", description="Portable computers")
    cctv = create_category(db, name="CCTV", description="Surveillance equipment")
    desktops = create_category(db, name="Desktops", description="Powerful desktops")

    # Brands
    acme = create_brand(db, name="ACME", description="Quality electronics")
    vision = create_brand(db, name="VisionTech", description="Security solutions")

    # Products
    create_product(
        db,
        name="ACME ProBook 15",
        description="15-inch powerful laptop",
        price_cents=129999,
        currency="USD",
        stock=10,
        image_url=None,
        category_id=laptops.id,
        brand_id=acme.id,
    )
    create_product(
        db,
        name="VisionTech 4K Camera",
        description="Outdoor 4K CCTV camera",
        price_cents=59999,
        currency="USD",
        stock=25,
        image_url=None,
        category_id=cctv.id,
        brand_id=vision.id,
    )
    create_product(
        db,
        name="ACME PowerStation",
        description="High-end desktop",
        price_cents=179999,
        currency="USD",
        stock=5,
        image_url=None,
        category_id=desktops.id,
        brand_id=acme.id,
    )
