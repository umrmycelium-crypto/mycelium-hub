from mycelium.core.constitution_human_override import get_request
from mycelium.core.constitution_mutation_commit import commit_mutation
from mycelium.core.constitution_mutation import get_proposal


def resume_with_human_decision(request_id):
    request = get_request(request_id)

    if not request:
        return {"status": "error", "reason": "invalid_request"}

    if request["status"] != "approve":
        return {"status": "blocked", "reason": "human_rejected"}

    proposal_id = request["proposal_id"]
    proposal = get_proposal(proposal_id)

    if not proposal:
        return {"status": "error", "reason": "proposal_missing"}

    return commit_mutation(proposal["change"], proposal_id)
