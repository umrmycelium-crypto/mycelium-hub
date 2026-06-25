from collections import defaultdict


def resolve_weighted_consensus(votes, quorum=0.65):
    """
    Weighted constitutional decision engine
    """

    total_weight = 0.0
    yes_weight = 0.0
    no_weight = 0.0

    breakdown = defaultdict(float)

    for v in votes:
        w = v.get("weight", 0)

        total_weight += w

        if v["vote"] == "YES":
            yes_weight += w
        elif v["vote"] == "NO":
            no_weight += w

        breakdown[v["vote"]] += w

    if total_weight == 0:
        return {"approved": False, "reason": "no_weight"}

    yes_ratio = yes_weight / total_weight

    return {
        "approved": yes_ratio >= quorum,
        "yes_ratio": yes_ratio,
        "total_weight": total_weight,
        "breakdown": dict(breakdown)
    }
