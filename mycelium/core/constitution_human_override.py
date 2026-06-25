import time

PENDING_HUMAN_REVIEW = {}


def create_review_request(proposal_id, simulation, validation):
    request_id = f"human-{proposal_id}"

    PENDING_HUMAN_REVIEW[request_id] = {
        "proposal_id": proposal_id,
        "simulation": simulation,
        "validation": validation,
        "status": "pending",
        "created_at": time.time(),
        "decision": None
    }

    return request_id


def get_request(request_id):
    return PENDING_HUMAN_REVIEW.get(request_id)


def set_decision(request_id, decision, reason=""):
    """
    decision: approve | reject
    """

    if request_id not in PENDING_HUMAN_REVIEW:
        return {"status": "error", "reason": "not_found"}

    PENDING_HUMAN_REVIEW[request_id]["status"] = decision
    PENDING_HUMAN_REVIEW[request_id]["decision"] = reason
    PENDING_HUMAN_REVIEW[request_id]["decided_at"] = time.time()

    return PENDING_HUMAN_REVIEW[request_id]
