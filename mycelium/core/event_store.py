import json
import os
import time

EVENT_LOG = "mycelium/logs/event_store.jsonl"


def append_event(event):
    """
    Canonical event persistence layer.
    Normalizes all incoming events into replay-compatible format.
    """

    os.makedirs("mycelium/logs", exist_ok=True)

    # Normalize event into a single stable schema
    record = {
        "timestamp": event.get("ts", time.time()),
        "event": event.get("type"),
        "payload": event.get("payload", {}),
        "results": event.get("results", [])
    }

    with open(EVENT_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")


def read_events():
    """
    Loads all events in canonical replay format.
    """

    if not os.path.exists(EVENT_LOG):
        return []

    events = []

    with open(EVENT_LOG, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                continue

    return events

from mycelium.core.secure_ledger import append_secure_event

def append_event_secure(event):
    return append_secure_event(event)
