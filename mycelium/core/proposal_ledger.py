from dataclasses import dataclass, asdict
from time import time
from typing import Dict, Any, List


PROPOSAL_LEDGER: List[Dict[str, Any]] = []


def submit_proposal(proposal: dict):
    proposal = {
        **proposal,
        "status": "proposed",
        "timestamp": time(),
        "id": len(PROPOSAL_LEDGER) + 1
    }
    PROPOSAL_LEDGER.append(proposal)
    return proposal


def list_proposals():
    return PROPOSAL_LEDGER


def get_proposal(pid: int):
    for p in PROPOSAL_LEDGER:
        if p["id"] == pid:
            return p
    return None


def update_proposal(pid: int, patch: dict):
    for p in PROPOSAL_LEDGER:
        if p["id"] == pid:
            p.update(patch)
            return p
    return None
