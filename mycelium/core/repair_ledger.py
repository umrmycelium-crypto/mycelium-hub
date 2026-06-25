import time

LEDGER = []


def log_repair(event):
    event["timestamp"] = time.time()
    LEDGER.append(event)


def get_history(limit=50):
    return LEDGER[-limit:]


def last_good_state():
    for e in reversed(LEDGER):
        if e.get("status") == "applied":
            return e
    return None
