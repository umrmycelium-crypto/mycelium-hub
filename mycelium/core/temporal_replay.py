from mycelium.core.event_store import read_events
from copy import deepcopy


def replay_until(timestamp: float):
    events = read_events()

    state = {
        "registry": {},
        "events": []
    }

    for e in events:
        if e.get("timestamp", 0) > timestamp:
            break

        state["events"].append(deepcopy(e))

        # minimal projection logic (safe mode only)
        if e.get("event") == "intent.executed":
            intent = e.get("payload", {}).get("intent")
            state["registry"][intent] = "executed"

    return {
        "status": "OK",
        "state_at_time": timestamp,
        "snapshot": state
    }


def system_replay(payload, context):
    return replay_until(payload.get("timestamp", 0))
