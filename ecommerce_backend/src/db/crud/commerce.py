from typing import Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException

from src.db.models.commerce import Cart, CartItem, Order, OrderItem
from src.db.models.catalog import Product


# PUBLIC_INTERFACE
def get_or_create_active_cart(db: Session, user_id: int) -> Cart:
    """Return user's active cart, creating one if missing."""
    cart: Optional[Cart] = db.execute(
        select(Cart).where(Cart.user_id == user_id, Cart.status == "active")
    ).scalars().first()
    if cart:
        return cart
    cart = Cart(user_id=user_id, status="active")
    db.add(cart)
    db.commit()
    db.refresh(cart)
    return cart


# PUBLIC_INTERFACE
def get_cart_with_items(db: Session, user_id: int) -> Cart:
    """Return the current active cart with items for a user (creates if missing)."""
    cart = get_or_create_active_cart(db, user_id)
    # Ensure items are loaded
    _ = cart.items
    return cart


def _get_cart_item(db: Session, cart_id: int, product_id: int) -> Optional[CartItem]:
    return db.execute(
        select(CartItem).where(CartItem.cart_id == cart_id, CartItem.product_id == product_id)
    ).scalars().first()


# PUBLIC_INTERFACE
def add_to_cart(db: Session, user_id: int, product_id: int, quantity: int = 1) -> Cart:
    """Add a product to the user's active cart, enforcing stock."""
    if quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be positive")

    cart = get_or_create_active_cart(db, user_id)
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    existing = _get_cart_item(db, cart.id, product_id)
    desired_qty = quantity + (existing.quantity if existing else 0)

    if product.stock < desired_qty:
        raise HTTPException(status_code=400, detail="Insufficient stock")

    if existing:
        existing.quantity = desired_qty
    else:
        db.add(CartItem(cart_id=cart.id, product_id=product_id, quantity=quantity))

    db.commit()
    db.refresh(cart)
    return cart


# PUBLIC_INTERFACE
def update_cart_item(db: Session, user_id: int, product_id: int, quantity: int) -> Cart:
    """Update quantity for a cart item, enforcing stock; if quantity<=0 removes item."""
    cart = get_or_create_active_cart(db, user_id)
    item = _get_cart_item(db, cart.id, product_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found in cart")

    if quantity <= 0:
        db.delete(item)
        db.commit()
        db.refresh(cart)
        return cart

    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.stock < quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")

    item.quantity = quantity
    db.commit()
    db.refresh(cart)
    return cart


# PUBLIC_INTERFACE
def remove_from_cart(db: Session, user_id: int, product_id: int) -> Cart:
    """Remove a product from cart."""
    cart = get_or_create_active_cart(db, user_id)
    item = _get_cart_item(db, cart.id, product_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found in cart")
    db.delete(item)
    db.commit()
    db.refresh(cart)
    return cart


def _calculate_cart_totals(db: Session, cart: Cart) -> Tuple[int, str]:
    """Calculate total cents and currency based on product prices."""
    if not cart.items:
        return 0, "USD"
    total = 0
    currency = "USD"
    for it in cart.items:
        product = db.get(Product, it.product_id)
        if product:
            total += product.price_cents * it.quantity
            currency = product.currency or currency
    return total, currency


# PUBLIC_INTERFACE
def checkout_cart(db: Session, user_id: int) -> Order:
    """Convert active cart into an order while enforcing stock and decrementing inventory."""
    cart = get_or_create_active_cart(db, user_id)
    if not cart.items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    # Validate stock
    for it in cart.items:
        product = db.get(Product, it.product_id)
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {it.product_id} not found")
        if product.stock < it.quantity:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for {product.name}")

    total_cents, currency = _calculate_cart_totals(db, cart)

    order = Order(user_id=user_id, status="paid", total_cents=total_cents, currency=currency)
    db.add(order)
    db.flush()  # obtain order.id

    # Create order items and adjust stock
    for it in cart.items:
        product = db.get(Product, it.product_id)
        product.stock -= it.quantity
        db.add(OrderItem(order_id=order.id, product_id=it.product_id, quantity=it.quantity, unit_price_cents=product.price_cents))

    # Close cart
    cart.status = "checked_out"
    db.commit()
    db.refresh(order)
    return order


# PUBLIC_INTERFACE
def list_user_orders(db: Session, user_id: int):
    """List orders for a user, most recent first."""
    return db.query(Order).filter(Order.user_id == user_id).order_by(Order.id.desc()).all()
