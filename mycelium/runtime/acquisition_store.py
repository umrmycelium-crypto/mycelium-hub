import json
import os
import time

STORE_PATH = "mycelium/logs/acquisition_state.jsonl"


def _ensure_file():
    os.makedirs(os.path.dirname(STORE_PATH), exist_ok=True)
    if not os.path.exists(STORE_PATH):
        open(STORE_PATH, "w").close()


def _append(event: dict):
    _ensure_file()
    with open(STORE_PATH, "a") as f:
        f.write(json.dumps(event) + "\n")


def record_request(title: str, status: str, payload=None):
    event = {
        "timestamp": time.time(),
        "title": title.lower().strip(),
        "status": status,  # REQUESTED | COMPLETED | FAILED
        "payload": payload or {}
    }
    _append(event)


def load_active_requests():
    _ensure_file()
    active = {}

    with open(STORE_PATH, "r") as f:
        for line in f:
            try:
                e = json.loads(line)
                if e["status"] == "REQUESTED":
                    active[e["title"]] = e
            except:
                continue

    return active


def is_already_requested(title: str) -> bool:
    active = load_active_requests()
    return title.lower().strip() in active
