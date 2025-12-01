from pydantic import BaseModel, Field


class Message(BaseModel):
    """Generic message response."""
    message: str = Field(..., description="Response message")
