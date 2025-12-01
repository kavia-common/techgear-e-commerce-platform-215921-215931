from pydantic import BaseModel, Field
from typing import Optional


class CategoryBase(BaseModel):
    name: str = Field(..., description="Category name")
    description: Optional[str] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryOut(CategoryBase):
    id: int

    class Config:
        from_attributes = True


class BrandBase(BaseModel):
    name: str
    description: Optional[str] = None


class BrandCreate(BrandBase):
    pass


class BrandOut(BrandBase):
    id: int

    class Config:
        from_attributes = True


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price_cents: int = 0
    currency: str = "USD"
    stock: int = 0
    image_url: Optional[str] = None
    category_id: Optional[int] = None
    brand_id: Optional[int] = None


class ProductCreate(ProductBase):
    pass


class ProductOut(ProductBase):
    id: int

    class Config:
        from_attributes = True
