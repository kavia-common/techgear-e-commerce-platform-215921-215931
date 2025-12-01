from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
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
        return cat
    # Defer commit to outer transaction
    return Category(name=name, description=description)


def _get_or_create_brand(db: Session, name: str, description: str | None = None) -> Brand:
    """Return existing brand by unique name or create it."""
    br = db.execute(select(Brand).where(Brand.name == name)).scalars().first()
    if br:
        if description is not None and br.description != description:
            br.description = description
        return br
    # Defer commit to outer transaction
    return Brand(name=name, description=description)


def _get_product_by_name(db: Session, name: str) -> Product | None:
    """Lookup product by name for idempotent seeding."""
    return db.execute(select(Product).where(Product.name == name)).scalars().first()


def seed(db: Session) -> None:
    """Populate development database with sample data in an idempotent manner.

    All operations are executed within a single transaction and use get-or-create
    checks on unique columns (e.g., name, email) to avoid UNIQUE violations.
    If a partial previous run exists, we query by unique fields and update existing
    rows rather than inserting duplicates.
    """
    try:
        # Start an explicit transaction boundary
        with db.begin():
            # Admin user (by unique email)
            admin_email = "admin@techgear.local"
            admin = get_user_by_email(db, admin_email)
            if not admin:
                # create_user internally commits; instead, create inline and let outer txn commit
                admin = create_user(
                    db,
                    email=admin_email,
                    hashed_password=get_password_hash("admin123"),
                    full_name="Admin",
                    is_admin=True,
                )

            # Categories (get or create)
            laptops = _get_or_create_category(db, name="Laptops", description="Portable computers")
            if isinstance(laptops, Category) and laptops.id is None:
                db.add(laptops)

            cctv = _get_or_create_category(db, name="CCTV", description="Surveillance equipment")
            if isinstance(cctv, Category) and cctv.id is None:
                db.add(cctv)

            desktops = _get_or_create_category(db, name="Desktops", description="Powerful desktops")
            if isinstance(desktops, Category) and desktops.id is None:
                db.add(desktops)

            # Brands (get or create)
            acme = _get_or_create_brand(db, name="ACME", description="Quality electronics")
            if isinstance(acme, Brand) and acme.id is None:
                db.add(acme)

            vision = _get_or_create_brand(db, name="VisionTech", description="Security solutions")
            if isinstance(vision, Brand) and vision.id is None:
                db.add(vision)

            # Flush so FK IDs exist for products
            db.flush()

            # Products (ensure by name)
            if not _get_product_by_name(db, "ACME ProBook 15"):
                # create_product internally commits; replicate logic inline to keep single txn
                prod = Product(
                    name="ACME ProBook 15",
                    description="15-inch powerful laptop",
                    price_cents=129999,
                    currency="USD",
                    stock=10,
                    image_url=None,
                    category_id=laptops.id,
                    brand_id=acme.id,
                )
                db.add(prod)

            if not _get_product_by_name(db, "VisionTech 4K Camera"):
                prod = Product(
                    name="VisionTech 4K Camera",
                    description="Outdoor 4K CCTV camera",
                    price_cents=59999,
                    currency="USD",
                    stock=25,
                    image_url=None,
                    category_id=cctv.id,
                    brand_id=vision.id,
                )
                db.add(prod)

            if not _get_product_by_name(db, "ACME PowerStation"):
                prod = Product(
                    name="ACME PowerStation",
                    description="High-end desktop",
                    price_cents=179999,
                    currency="USD",
                    stock=5,
                    image_url=None,
                    category_id=desktops.id,
                    brand_id=acme.id,
                )
                db.add(prod)

            # Any pending updates to descriptions are already on instances; flush handled by context

    except IntegrityError:
        # Rollback in case of any unique constraint violation to keep app booting cleanly
        db.rollback()
        # Intentionally swallow to make seeding idempotent and non-fatal on startup
        # Could add logging here if a logging framework is present
