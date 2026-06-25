from mycelium.core.intent import Intent
from mycelium.core.registry import REGISTRY


def validate_intent(intent: Intent):
    if intent.name not in REGISTRY:
        return {"ok": False, "reason": "UNKNOWN_INTENT"}

    if not (0.0 <= intent.confidence <= 1.0):
        return {"ok": False, "reason": "INVALID_CONFIDENCE"}

    if not isinstance(intent.payload, dict):
        return {"ok": False, "reason": "INVALID_PAYLOAD"}

    if not isinstance(intent.context, dict):
        return {"ok": False, "reason": "INVALID_CONTEXT"}

    return {"ok": True}
