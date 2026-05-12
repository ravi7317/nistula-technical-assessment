import uuid
from app.models.request_models import InboundMessage, UnifiedMessage

def normalize_message(inbound: InboundMessage) -> UnifiedMessage:
    """
    Normalizes different inbound sources into a UnifiedMessage schema.
    """
    return UnifiedMessage(
        message_id=str(uuid.uuid4()),
        source=inbound.source,
        guest_name=inbound.guest_name,
        message_text=inbound.message,
        timestamp=inbound.timestamp,
        booking_ref=inbound.booking_ref,
        property_id=inbound.property_id,
        query_type="pending"
    )
