from sqlalchemy.orm import Session
from sqlalchemy import select
from src.db.crud.catalog import create_brand, create_category, create_product
from src.db.crud.user import create_user, get_user_by_email
from src.core.security import get_password_hash
from src.db.models.catalog import Category, Brand, Product


def _get_or_create_category(db: Session, name: str, description: str | None = None) -> Category:
    """Return existing category by unique name or create it."""
    cat = db.execute(select(Category).where(Category.name == name)).scalars().first()
    if cat:
        # Optionally update description if provided and different
        if description is not None and cat.description != description:
            cat.description = description
            db.commit()
            db.refresh(cat)
        return cat
    return create_category(db, name=name, description=description)


def _get_or_create_brand(db: Session, name: str, description: str | None = None) -> Brand:
    """Return existing brand by unique name or create it."""
    br = db.execute(select(Brand).where(Brand.name == name)).scalars().first()
    if br:
        if description is not None and br.description != description:
            br.description = description
            db.commit()
            db.refresh(br)
        return br
    return create_brand(db, name=name, description=description)


def _get_product_by_name(db: Session, name: str) -> Product | None:
    return db.execute(select(Product).where(Product.name == name)).scalars().first()


def seed(db: Session) -> None:
    """Populate development database with sample data in an idempotent manner.

    This function uses get-or-create checks based on unique columns (like name)
    so running it multiple times won't violate UNIQUE constraints nor create duplicates.
    """
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

    # Categories (get or create)
    laptops = _get_or_create_category(db, name="Laptops", description="Portable computers")
    cctv = _get_or_create_category(db, name="CCTV", description="Surveillance equipment")
    desktops = _get_or_create_category(db, name="Desktops", description="Powerful desktops")

    # Brands (get or create)
    acme = _get_or_create_brand(db, name="ACME", description="Quality electronics")
    vision = _get_or_create_brand(db, name="VisionTech", description="Security solutions")

    # Products (ensure by name)
    if not _get_product_by_name(db, "ACME ProBook 15"):
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

    if not _get_product_by_name(db, "VisionTech 4K Camera"):
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

    if not _get_product_by_name(db, "ACME PowerStation"):
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
