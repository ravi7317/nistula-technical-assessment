from pydantic import BaseModel
from typing import Literal

class WebhookResponse(BaseModel):
    message_id: str
    query_type: str
    drafted_reply: str
    confidence_score: float
    action: Literal["auto_send", "agent_review", "escalate"]
