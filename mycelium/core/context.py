from pathlib import Path
import json

# Paths established in documentation and core modules
STATE_FILE = Path("docs/CURRENT_STATE.md")
EVENT_LOG = Path("mycelium/logs/event_log.jsonl")

def get_system_state():
    """
    Reads the authoritative system state from the documentation.
    """
    if STATE_FILE.exists():
        return STATE_FILE.read_text()
    return "SYSTEM STATE: Documentation file missing."

def get_recent_events(limit=10):
    """
    Retrieves the most recent N events from the event log for session context.
    """
    if not EVENT_LOG.exists():
        return []

    events = []
    try:
        with open(EVENT_LOG, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    events.append(json.loads(line))
    except Exception as e:
        print(f"Context Error: Failed to read event log: {e}")

    # Return only the most recent events
    return events[-limit:]
