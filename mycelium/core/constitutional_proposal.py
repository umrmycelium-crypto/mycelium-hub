import time
import uuid

PROPOSALS = {}


def create_proposal(change):
    pid = str(uuid.uuid4())

    PROPOSALS[pid] = {
        "id": pid,
        "change": change,
        "votes": [],
        "created_at": time.time()
    }

    return pid


def add_vote(pid, vote):
    if pid not in PROPOSALS:
        return False

    PROPOSALS[pid]["votes"].append(vote.to_dict())
    return True


def get_proposal(pid):
    return PROPOSALS.get(pid)
