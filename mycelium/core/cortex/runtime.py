import json

def parse_cortex_output(raw: str):
    try:
        data = json.loads(raw)
    except Exception:
        return {"ok": False, "error": "invalid_json"}

    if "intents" not in data:
        return {"ok": False, "error": "missing_intents"}

    for i in data["intents"]:
        if not (0.0 <= i["confidence"] <= 1.0):
            return {"ok": False, "error": "bad_confidence"}

    return {"ok": True, "data": data}
