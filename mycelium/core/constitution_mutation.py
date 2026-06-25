import uuid
import time

from mycelium.core.constitution_store import (
    CURRENT_CONSTITUTION,
    save_version
)

MUTATION_PROPOSALS = {}


def propose_mutation(change: dict, reason="unspecified"):
    """
    Create a constitutional change proposal.
    """

    pid = str(uuid.uuid4())

    MUTATION_PROPOSALS[pid] = {
        "id": pid,
        "change": change,
        "reason": reason,
        "status": "pending",
        "created_at": time.time()
    }

    return {
        "proposal_id": pid,
        "status": "created"
    }


def get_proposal(pid):
    return MUTATION_PROPOSALS.get(pid)
