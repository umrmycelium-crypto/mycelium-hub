from mycelium.core.event_bus import EVENT_BUS


def emit_reason(intent, stage, meta=None):
    """
    Adds interpretability to execution flow
    """

    EVENT_BUS.publish({
        "type": "system.reason",
        "payload": {
            "intent": intent.get("name"),
            "stage": stage,
            "meta": meta or {}
        }
    })
