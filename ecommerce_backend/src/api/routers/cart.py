from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session

from src.core.security import get_current_user
from src.db.schemas.common import Message
from src.db.schemas.commerce import CartOut, CartItemCreate
from src.db.session import get_db
from src.db.crud.commerce import (
    get_cart_with_items,
    add_to_cart,
    update_cart_item,
    remove_from_cart,
    checkout_cart,
)

router = APIRouter(prefix="/cart", tags=["Cart"])


@router.get(
    "/",
    response_model=CartOut,
    summary="Get current user's cart",
    description="Return active cart with items for the authenticated user.",
)
def get_cart(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    """Return active cart with items for the authenticated user."""
    return get_cart_with_items(db, current_user.id)


@router.post(
    "/items",
    response_model=CartOut,
    summary="Add item to cart",
    description="Add a product to the cart. Enforces stock availability.",
)
def add_item(
    payload: CartItemCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Add a product to the cart. Enforces stock availability."""
    return add_to_cart(db, current_user.id, payload.product_id, payload.quantity)


@router.put(
    "/items/{product_id}",
    response_model=CartOut,
    summary="Update cart item quantity",
    description="Update quantity of a product in the cart. Quantity <= 0 will remove the item.",
)
def update_item(
    product_id: int,
    quantity: int = Body(..., embed=True, description="New quantity"),
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update quantity for a cart item; if quantity <= 0 the item is removed."""
    return update_cart_item(db, current_user.id, product_id, quantity)


@router.delete(
    "/items/{product_id}",
    response_model=CartOut,
    summary="Remove item from cart",
    description="Remove a product from the cart.",
)
def remove_item(
    product_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Remove a product from the cart."""
    return remove_from_cart(db, current_user.id, product_id)


@router.post(
    "/checkout",
    response_model=Message,
    summary="Checkout cart",
    description="Create an order from the active cart, enforce stock, decrement inventory, and close cart.",
)
def checkout(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Checkout the active cart into an order."""
    order = checkout_cart(db, current_user.id)
    return Message(message=f"Order {order.id} placed successfully")
