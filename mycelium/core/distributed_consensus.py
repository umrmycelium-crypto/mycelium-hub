from mycelium.core.consensus_engine import evaluate_proposal

VOTERS = [
    "governance",
    "safety",
    "system",
]


def vote(proposal: dict):
    """
    Each voter casts a deterministic vote.
    """

    votes = {}

    base_score = evaluate_proposal(proposal)

    votes["governance"] = base_score >= 0.65
    votes["safety"] = proposal.get("risk") != "high"
    votes["system"] = proposal.get("confidence", 0) > 0.3

    approved = all(votes.values())

    return {
        "approved": approved,
        "votes": votes,
        "score": base_score
    }
