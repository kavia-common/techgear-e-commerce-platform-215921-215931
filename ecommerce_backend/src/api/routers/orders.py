from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.security import get_current_user
from src.db.schemas.commerce import OrderOut
from src.db.session import get_db
from src.db.crud.commerce import list_user_orders

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.get(
    "/",
    response_model=List[OrderOut],
    summary="List current user's orders",
    description="Return all orders for the authenticated user, most recent first.",
)
def list_orders(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    """Return all orders for the authenticated user."""
    return list_user_orders(db, current_user.id)
