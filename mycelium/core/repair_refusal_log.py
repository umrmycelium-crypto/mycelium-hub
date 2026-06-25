import json
import os
import time

LOG = "mycelium/logs/repair_refusals.jsonl"


def log_refusal(strategy: str, patch: str, reason: list):
    os.makedirs("mycelium/logs", exist_ok=True)

    with open(LOG, "a") as f:
        f.write(json.dumps({
            "ts": time.time(),
            "strategy": strategy,
            "patch": patch,
            "reason": reason
        }) + "\n")
