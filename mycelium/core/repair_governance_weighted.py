from mycelium.core.constitutional_weights import get_weight
from mycelium.core.constitutional_weighted_consensus import resolve_weighted_consensus


def weighted_governance(patch, agent_votes):
    """
    Weighted constitutional authority layer
    """

    enriched_votes = []

    for v in agent_votes:
        enriched_votes.append({
            "agent": v["agent"],
            "vote": v["vote"],
            "weight": get_weight(v["agent"]),
            "reason": v.get("reason", "")
        })

    consensus = resolve_weighted_consensus(enriched_votes)

    return {
        "allowed": consensus["approved"],
        "mode": "weighted_constitution",
        "consensus": consensus
    }
