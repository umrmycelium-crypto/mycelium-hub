import json

REQUIRED_KEYS = {"name", "confidence", "payload"}

def validate_cortex_output(raw: str):
    try:
        data = json.loads(raw)
    except Exception:
        return {"ok": False, "error": "invalid_json"}

    if "intents" not in data:
        return {"ok": False, "error": "missing_intents"}

    for intent in data["intents"]:
        if not REQUIRED_KEYS.issubset(intent.keys()):
            return {"ok": False, "error": "invalid_intent_shape"}

        if not (0.0 <= intent["confidence"] <= 1.0):
            return {"ok": False, "error": "invalid_confidence"}

    return {"ok": True, "data": data}
