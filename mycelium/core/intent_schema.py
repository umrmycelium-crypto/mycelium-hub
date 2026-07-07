INTENT_SCHEMAS = {
    "media.play": {
        "required": ["title"],
        "optional": []
    },
    "system.ping": {
        "required": [],
        "optional": []
    },
    "system.status": {
        "required": [],
        "optional": []
    }
}

def validate_intent(data: dict) -> dict:
    """
    Validates that the intent data matches the expected schema.
    """
    intent_name = data.get("intent")
    if not intent_name:
        raise ValueError("Intent data missing 'intent' field.")
    
    schema = INTENT_SCHEMAS.get(intent_name)
    if not schema:
        # Allow unknown intents to pass through for flexibility (can be refined later)
        return data
    
    payload = data.get("payload", {})
    for req in schema["required"]:
        if req not in payload:
            raise ValueError(f"Intent '{intent_name}' missing required payload field: {req}")
            
    return data
