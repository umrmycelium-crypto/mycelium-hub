from mycelium.core.registry import REGISTRY
from mycelium.core.validator import validate_intent
from mycelium.core.event_bus import EVENT_BUS


def execute(intent):
    validation = validate_intent(intent)

    if not validation["ok"]:
        return {
            "status": "REJECTED",
            "reason": validation["reason"]
        }

    handler = REGISTRY[intent.name]

    try:
        result = handler(intent.payload, intent.context)
    except Exception as e:
        result = {
            "status": "ERROR",
            "error": str(e)
        }

    EVENT_BUS.publish({
        "intent": intent.name,
        "payload": intent.payload,
        "result": result
    })

    return result
