"""
Mycelium Constitutional Layer v1
"""

ALLOWED_INTENTS = {
    "system.ping",
    "system.status",
    "system.events",
    "system.drift",
    "media.play",
    "ai.ask",
    "knowledge.query",
}

PROTECTED_INTENTS = {
    "system.governance",
}


def evaluate(intent: dict) -> dict:
    name = intent.get("name")

    # hard deny
    if name in PROTECTED_INTENTS:
        return {"decision": "DENY", "reason": "protected intent"}

    # allowed
    if name in ALLOWED_INTENTS:
        return {"decision": "ALLOW"}

    # unknown → review
    return {
        "decision": "REVIEW",
        "reason": "unknown intent",
        "suggested_action": "register_or_repair"
    }
