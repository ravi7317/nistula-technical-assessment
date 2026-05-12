from pydantic import BaseModel, Field
from typing import Literal
from datetime import datetime
import uuid

class InboundMessage(BaseModel):
    source: Literal["whatsapp", "booking_com", "airbnb", "instagram", "direct"]
    guest_name: str
    message: str
    timestamp: datetime
    booking_ref: str
    property_id: str

class UnifiedMessage(BaseModel):
    message_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    source: str
    guest_name: str
    message_text: str
    timestamp: datetime
    booking_ref: str
    property_id: str
    query_type: str
