from mycelium.core.event_store import read_events
from mycelium.core.proposal_ledger import submit_proposal


def mine_capabilities():
    events = read_events()

    suggestions = []

    for e in events[-50:]:
        raw = str(e.get("event", ""))

        # simple heuristic mining (safe baseline)
        if "intent.unhandled" in raw:
            payload = e.get("payload", {}).get("payload", {})
            raw_text = payload.get("raw")

            if raw_text:
                suggestions.append({
                    "name": f"auto.{raw_text.split()[0]}",
                    "reason": "frequent unknown intent pattern",
                    "confidence": 0.3,
                    "risk": "medium",
                    "intent_schema": {
                        "name": raw_text,
                        "payload": {},
                        "context": {}
                    }
                })

    created = []
    for s in suggestions:
        created.append(submit_proposal(s))

    return {
        "status": "OK",
        "mined": len(created),
        "proposals": created
    }
