from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserBase(BaseModel):
    """Base user properties shared across schemas."""
    email: EmailStr = Field(..., description="User email address")
    full_name: Optional[str] = Field(None, description="Full name of the user")


class UserCreate(UserBase):
    """Schema for user registration."""
    password: str = Field(..., min_length=6, description="Plain password")


class UserLogin(BaseModel):
    """Schema for login credentials."""
    email: EmailStr
    password: str


class UserOut(UserBase):
    """User info exposed in API responses."""
    id: int
    is_active: bool
    is_admin: bool

    class Config:
        from_attributes = True


class Token(BaseModel):
    """JWT access token response."""
    access_token: str
    token_type: str = "bearer"
