from fastapi import APIRouter, Depends
from src.core.security import get_current_user
from src.db.schemas.common import Message

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.get("/", response_model=Message, summary="List current user's orders")
def list_orders(_: str = Depends(get_current_user)):
    """
    Placeholder endpoint for listing current user's orders.
    """
    return Message(message="Order endpoints will be implemented in the next step.")
