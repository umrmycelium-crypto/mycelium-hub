from mycelium.core.proposal_ledger import get_proposal


def evaluate_proposal(proposal: dict):
    """
    Deterministic scoring gate.
    """

    score = 0.0

    # confidence weight
    score += proposal.get("confidence", 0) * 0.5

    # risk penalty
    risk = proposal.get("risk", "medium")
    if risk == "low":
        score += 0.3
    elif risk == "medium":
        score += 0.1
    else:
        score -= 0.4

    # heuristic safety checks
    name = proposal.get("name", "")
    if name.startswith("auto."):
        score -= 0.1

    return score


def consensus_check(proposal: dict):
    """
    Final gate: must exceed threshold.
    """

    score = evaluate_proposal(proposal)

    return {
        "approved": score >= 0.6,
        "score": score,
        "threshold": 0.6
    }
