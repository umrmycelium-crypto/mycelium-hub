from mycelium.core.event_store import read_events
from mycelium.core.event_bus import EVENT_BUS


def analyze_recent_failures(limit=50):
    events = read_events()[-limit:]
    return [e for e in events if e.get("type") in ("intent.failed", "acquisition.failed")]


def suggest_repair():
    failures = analyze_recent_failures()

    if not failures:
        return

    intent_counts = {}

    for f in failures:
        intent = f.get("payload", {}).get("intent", "unknown")
        intent_counts[intent] = intent_counts.get(intent, 0) + 1

    dominant = max(intent_counts.items(), key=lambda x: x[1], default=None)

    if not dominant:
        return

    intent_name, count = dominant

    EVENT_BUS.publish({
        "type": "system.repair.suggested",
        "payload": {
            "intent": intent_name,
            "severity": "high" if count > 3 else "medium",
            "auto_apply": False
        }
    })


def suggest_auto_patch(intent_name):
    """
    placeholder hook for AI-generated patch injection
    """
    return {
        "path": "UNKNOWN",
        "content": "",
        "auto_apply": False
    }
