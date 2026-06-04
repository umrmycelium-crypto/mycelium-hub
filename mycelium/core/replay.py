import json
from pathlib import Path

# Use the same log file path established in the logger module
LOG_FILE = Path("mycelium/logs/event_log.jsonl")

def load_events():
    """
    Loads all events from the persistent JSONL log.
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

def replay(bus, filter_event=None):
    """
    Re-publishes logged events to the bus and collects the results.
    """
    events = load_events()
    replay_trace = []

    for event in events:
        event_type = event.get("event")
        
        if filter_event and event_type != filter_event:
            continue
            
        payload = event.get("payload", {})
        
        # Publish back to the bus to trigger current handlers
        results = bus.publish(event_type, payload)
        
        replay_trace.append({
            "original_timestamp": event.get("timestamp"),
            "event": event_type,
            "payload": payload,
            "replayed_results": results
        })

    return replay_trace
