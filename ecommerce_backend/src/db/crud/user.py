from sqlalchemy.orm import Session
from typing import Optional
from src.db.models.user import User


# PUBLIC_INTERFACE
def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Return a user by email if exists."""
    return db.query(User).filter(User.email == email).first()


# PUBLIC_INTERFACE
def create_user(db: Session, email: str, hashed_password: str, full_name: str | None = None, is_admin: bool = False) -> User:
    """Create a new user with hashed password."""
    user = User(email=email, hashed_password=hashed_password, full_name=full_name, is_admin=is_admin)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
