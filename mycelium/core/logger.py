import json
from datetime import datetime, timezone
from pathlib import Path

# Log file path relative to project root
LOG_FILE = Path("mycelium/logs/event_log.jsonl")

def log_event(event_type, payload, results):
    """
    Appends a structured event entry to the JSONL log file.
    """
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event": event_type,
        "payload": payload,
        "results": results
    }

    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception as e:
        print(f"Logging Error: {e}")

    return entry
