from collections import Counter


def resolve_consensus(votes, quorum=0.66):
    """
    Distributed constitutional decision.
    """

    if not votes:
        return {"approved": False, "reason": "no_votes"}

    tally = Counter(v["vote"] for v in votes)

    total = sum(tally.values())
    yes = tally.get("YES", 0)

    ratio = yes / total if total > 0 else 0

    return {
        "approved": ratio >= quorum,
        "yes_ratio": ratio,
        "total_votes": total,
        "breakdown": dict(tally)
    }
