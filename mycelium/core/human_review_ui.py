from mycelium.core.constitution_human_override import PENDING_HUMAN_REVIEW
import json


def list_pending_reviews():
    return [
        {
            "request_id": k,
            "proposal_id": v["proposal_id"],
            "status": v["status"],
            "created_at": v["created_at"]
        }
        for k, v in PENDING_HUMAN_REVIEW.items()
    ]


def view_request(request_id):
    req = PENDING_HUMAN_REVIEW.get(request_id)

    if not req:
        return {"status": "error", "reason": "not_found"}

    return {
        "request_id": request_id,
        "proposal_id": req["proposal_id"],
        "simulation": req["simulation"],
        "validation": req["validation"],
        "status": req["status"],
        "decision": req.get("decision")
    }
