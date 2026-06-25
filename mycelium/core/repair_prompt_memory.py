import json
import os
import time

PROMPT_LOG = "mycelium/logs/repair_prompts.jsonl"


def record(prompt: str, drift: dict, patch: dict, score: float):
    os.makedirs("mycelium/logs", exist_ok=True)

    entry = {
        "ts": time.time(),
        "prompt": prompt,
        "drift": drift,
        "patch": patch,
        "score": score
    }

    with open(PROMPT_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")


def load_all():
    if not os.path.exists(PROMPT_LOG):
        return []

    with open(PROMPT_LOG) as f:
        return [json.loads(x) for x in f if x.strip()]
