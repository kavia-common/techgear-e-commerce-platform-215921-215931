from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.db.schemas.user import UserCreate, UserLogin, UserOut, Token
from src.db.crud.user import get_user_by_email, create_user
from src.db.session import get_db
from src.core.security import verify_password, get_password_hash, create_access_token, get_current_user
from src.db.models.user import User

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserOut, summary="Register a new user")
def register(payload: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.

    - email: unique email address
    - password: minimum 6 characters
    """
    existing = get_user_by_email(db, payload.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = create_user(
        db,
        email=payload.email,
        hashed_password=get_password_hash(payload.password),
        full_name=payload.full_name,
        is_admin=False,
    )
    return user


@router.post("/login", response_model=Token, summary="Login and receive JWT")
def login(payload: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate user and issue JWT access token.
    """
    user = get_user_by_email(db, payload.email)
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token(subject=user.email)
    return Token(access_token=token)


@router.get("/me", response_model=UserOut, summary="Get current authenticated user")
def me(current_user: User = Depends(get_current_user)):
    """
    Return the current authenticated user.
    """
    return current_user
