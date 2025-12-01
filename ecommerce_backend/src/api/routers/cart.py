from fastapi import APIRouter, Depends
from src.core.security import get_current_user
from src.db.schemas.common import Message

router = APIRouter(prefix="/cart", tags=["Cart"])


@router.get("/", response_model=Message, summary="Get current user's cart")
def get_cart(_: str = Depends(get_current_user)):
    """
    Placeholder endpoint for getting the current user's cart.
    """
    return Message(message="Cart endpoints will be implemented in the next step.")
