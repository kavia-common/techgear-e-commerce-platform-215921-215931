from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.config import get_settings
from src.db.session import Base, engine
from src.db.session import get_db  # noqa: F401 ensure dependency is importable
from src.db.init_db import seed

from src.api.routers.auth import router as auth_router
from src.api.routers.products import router as products_router
from src.api.routers.categories import router as categories_router
from src.api.routers.brands import router as brands_router
from src.api.routers.cart import router as cart_router
from src.api.routers.orders import router as orders_router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables
    Base.metadata.create_all(bind=engine)
    # Seed data in dev if configured
    if settings.SEED_DATA_ON_STARTUP and settings.DATABASE_URL.startswith("sqlite"):
        from sqlalchemy.orm import Session
        db = Session(bind=engine, future=True)
        try:
            seed(db)
        finally:
            db.close()
    yield
    # No teardown actions for now


app = FastAPI(
    title=settings.APP_NAME,
    description="E-commerce backend API",
    version=settings.API_VERSION,
    lifespan=lifespan,
    openapi_tags=[
        {"name": "Auth", "description": "Authentication endpoints"},
        {"name": "Products", "description": "Product catalogue"},
        {"name": "Categories", "description": "Product categories"},
        {"name": "Brands", "description": "Product brands"},
        {"name": "Cart", "description": "Shopping cart"},
        {"name": "Orders", "description": "Orders and checkout"},
    ],
)

# CORS: allow frontend on localhost:3000 by default
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", summary="Health Check", tags=["Auth"])
def health_check():
    """Return basic health status."""
    return {"message": "Healthy"}


# Register routers
app.include_router(auth_router)
app.include_router(products_router)
app.include_router(categories_router)
app.include_router(brands_router)
app.include_router(cart_router)
app.include_router(orders_router)
