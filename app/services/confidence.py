def determine_action(confidence_score: float, query_type: str) -> str:
    """
    Business logic for routing messages. 
    Complaints are always escalated to humans, as are low-confidence responses.
    Medium confidence allows for an agent review, while high confidence auto-sends.
    """
    if query_type == "complaint" or confidence_score < 0.60:
        return "escalate"
    if 0.60 <= confidence_score <= 0.85:
        return "agent_review"
    return "auto_send"
