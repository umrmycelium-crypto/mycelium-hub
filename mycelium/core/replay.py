import json
from pathlib import Path
from .diff import diff_events

# Canonical event log (must match event_store.py)
LOG_FILE = Path("mycelium/logs/event_store.jsonl")


# -----------------------------
# Event Loading
# -----------------------------

def load_events():
    """
    Loads all persisted events from JSONL log.
    Returns canonical event format:
    {
        "timestamp": float,
        "event": str,
        "payload": dict,
        "results": list
    }
    """

    events = []

    if not LOG_FILE.exists():
        return events

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                continue

    return events


# -----------------------------
# Behavioral Replay (legacy / optional)
# -----------------------------

def replay(bus, filter_event=None):
    """
    Replays events through the bus (for regression testing).
    NOTE: This executes handlers and compares outputs.
    """

    events = load_events()
    replay_trace = []

    for event in events:
        event_type = event.get("event")

        if filter_event and event_type != filter_event:
            continue

        payload = event.get("payload", {})
        original_results = event.get("results", [])

        # IMPORTANT:
        # We assume bus.publish supports (event dict)
        replayed_results = bus.publish({
            "type": event_type,
            "payload": payload
        })

        comparison = diff_events(original_results, replayed_results)

        replay_trace.append({
            "timestamp": event.get("timestamp"),
            "event": event_type,
            "payload": payload,
            "diff": comparison
        })

    return replay_trace


# -----------------------------
# State Replay (RFC-012 core)
# -----------------------------

def replay_state_only():
    """
    Rebuilds system state deterministically from event log.
    Used for system.drift comparisons.
    """

    events = load_events()

    state = {
        "requests": {},
        "system": {}
    }

    for event in events:
        event_type = event.get("event")
        payload = event.get("payload", {})

        # Acquisition lifecycle
        if event_type == "acquisition.requested":
            state["requests"][payload["title"]] = "REQUESTED"

        elif event_type == "acquisition.available":
            state["requests"][payload["title"]] = "AVAILABLE"

        elif event_type == "acquisition.completed":
            state["requests"][payload["title"]] = "COMPLETED"

        # System lifecycle
        elif event_type == "system.started":
            state["system"]["started"] = True

    return state
