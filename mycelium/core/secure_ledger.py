import hashlib
import json
from time import time

LEDGER = []


def _hash(data: str):
    return hashlib.sha256(data.encode()).hexdigest()


def append_secure_event(event: dict):
    prev_hash = LEDGER[-1]["hash"] if LEDGER else "GENESIS"

    payload = {
        "event": event,
        "prev": prev_hash,
        "timestamp": time()
    }

    payload_str = json.dumps(payload, sort_keys=True)

    event_hash = _hash(payload_str)

    block = {
        "data": payload,
        "hash": event_hash
    }

    LEDGER.append(block)

    return block


def verify_chain():
    for i in range(1, len(LEDGER)):
        prev = LEDGER[i - 1]["hash"]
        if LEDGER[i]["data"]["prev"] != prev:
            return {"valid": False, "index": i}

    return {"valid": True}


def system_ledger_status(payload, context):
    return {
        "blocks": len(LEDGER),
        "valid": verify_chain()
    }
