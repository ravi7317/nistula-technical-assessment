QUERY_TYPES = [
    "pre_sales_availability",
    "pre_sales_pricing",
    "post_sales_checkin",
    "special_request",
    "complaint",
    "general_enquiry"
]

def get_classification_prompt_context():
    return f"Classify the guest message into one of these types: {', '.join(QUERY_TYPES)}."
