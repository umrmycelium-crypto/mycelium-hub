import time
import uuid

PROPOSALS = []


def propose_change(rule_key, new_value, reason, author="repair_system"):
    proposal = {
        "id": str(uuid.uuid4()),
        "rule": rule_key,
        "new_value": new_value,
        "reason": reason,
        "author": author,
        "timestamp": time.time(),
        "status": "pending"
    }

    PROPOSALS.append(proposal)
    return proposal


def get_proposals(status=None):
    if status:
        return [p for p in PROPOSALS if p["status"] == status]
    return PROPOSALS
