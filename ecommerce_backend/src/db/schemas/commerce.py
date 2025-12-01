from pydantic import BaseModel
from typing import List


class CartItemBase(BaseModel):
    product_id: int
    quantity: int = 1


class CartItemCreate(CartItemBase):
    pass


class CartItemOut(CartItemBase):
    id: int

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
