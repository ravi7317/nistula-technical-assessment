from fastapi import APIRouter
from app.models.request_models import InboundMessage
from app.models.response_models import WebhookResponse
from app.services.claude_service import get_claude_response
from app.services.normalizer import normalize_message
from app.services.confidence import determine_action

router = APIRouter()

@router.post("/webhook/message", response_model=WebhookResponse)
async def handle_webhook(inbound: InboundMessage):
    # Map the inbound payload to our internal unified schema
    unified_msg = normalize_message(inbound)

    # Hand off to Claude for classification and drafting a reply
    ai_data = await get_claude_response(unified_msg)
    
    # Extract results from AI response
    query_type = ai_data.get("query_type", "general_enquiry")
    confidence = ai_data.get("confidence_score", 0.0)
    
    # Route the action based on how confident the AI is
    action = determine_action(confidence, query_type)

    return WebhookResponse(
        message_id=unified_msg.message_id,
        query_type=query_type,
        drafted_reply=ai_data.get("drafted_reply", ""),
        confidence_score=confidence,
        action=action
    )
