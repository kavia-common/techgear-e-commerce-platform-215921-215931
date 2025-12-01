from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from typing import Generator
from src.core.config import get_settings

settings = get_settings()

# SQLite specific connect args
connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(settings.DATABASE_URL, echo=False, future=True, connect_args=connect_args)


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models."""
    pass


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)


# PUBLIC_INTERFACE
def get_db() -> Generator:
    """FastAPI dependency that provides a SQLAlchemy session and ensures cleanup."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
