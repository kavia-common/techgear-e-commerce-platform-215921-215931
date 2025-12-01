from typing import List, Optional
from pydantic import BaseModel


class CartItemBase(BaseModel):
    product_id: int
    quantity: int = 1


class CartItemCreate(CartItemBase):
    """Payload for adding items to cart."""
    pass


class ProductBrief(BaseModel):
    id: int
    name: str
    price_cents: int
    currency: str
    stock: int
    image_url: Optional[str] = None

    class Config:
        from_attributes = True


class CartItemOut(CartItemBase):
    id: int
    product: Optional[ProductBrief] = None

    class Config:
        from_attributes = True


class CartOut(BaseModel):
    id: int
    status: str
    items: List[CartItemOut] = []

    class Config:
        from_attributes = True


class OrderItemOut(BaseModel):
    id: int
    product_id: int
    quantity: int
    unit_price_cents: int
    product: Optional[ProductBrief] = None

    class Config:
        from_attributes = True


class OrderOut(BaseModel):
    id: int
    status: str
    total_cents: int
    currency: str
    items: List[OrderItemOut] = []

    class Config:
        from_attributes = True
