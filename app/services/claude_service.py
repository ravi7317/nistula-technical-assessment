import anthropic
import json
from app.config import Config
from app.models.request_models import UnifiedMessage

client = anthropic.Anthropic(api_key=Config.ANTHROPIC_API_KEY)

MOCK_PROPERTY_CONTEXT = """
Property: Villa B1, Assagao, North Goa
Bedrooms: 3 | Max guests: 6 | Private pool: Yes
Check-in: 2pm | Check-out: 11am
Base rate: INR 18,000 per night (up to 4 guests)
Extra guest: INR 2,000 per night per person
WiFi password: Nistula@2024
Caretaker: Available 8am to 10pm
Chef on call: Yes, pre-booking required
Availability April 20-24: Available
Cancellation: Free up to 7 days before check-in
"""

from app.services.classifier import QUERY_TYPES

async def get_claude_response(unified_msg: UnifiedMessage):
    prompt = f"""
    You are an AI assistant for Nistula, a premium villa management company.
    Your task is to:
    1. Classify the guest message into one of these types: {', '.join(QUERY_TYPES)}.
    2. Draft a concise, conversational, and WhatsApp-native reply based on the provided Property Context.
       - Keep it mobile-friendly and helpful.
       - Address the guest by name.
       - Avoid explicitly mentioning years in dates (e.g., use "April 20 to 24").
    3. Provide a realistic probabilistic confidence score (0.0 to 0.98). 
       - Avoid artificial perfection; never return exactly 1.0.
       - A high-quality match should be between 0.90 and 0.95.

    Property Context:
    {MOCK_PROPERTY_CONTEXT}

    Guest Message:
    Name: {unified_msg.guest_name}
    Message: {unified_msg.message_text}

    Return the result in JSON format with exactly these keys:
    "query_type": "one of the types listed above",
    "drafted_reply": "your drafted message",
    "confidence_score": 0.92
    """

    try:
        response = client.messages.create(
            model=Config.CLAUDE_MODEL,
            max_tokens=1000,
            system="You are a helpful, concise hospitality assistant for Nistula. You respond only in valid JSON. Your tone is WhatsApp-native: professional yet warm and brief.",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        raw_content = response.content[0].text
        content = raw_content.strip()
        
        # Simple cleanup in case Claude wraps the JSON in markdown blocks
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        
        # Handle cases where splitting might result in an empty string
        if not content:
            content = raw_content.strip()
            
        return json.loads(content)

    except Exception as e:
        # Log the error and return a safe fallback for the agent
        print(f"DEBUG: Claude API error: {e}")
        return {
            "query_type": "general_enquiry",
            "drafted_reply": "I'm sorry, I'm having a bit of trouble processing that. Our team will get back to you shortly!",
            "confidence_score": 0.0
        }
