from mycelium.core.repair_guard import is_allowed


def constitutional_score(pre_score: float, patch: str) -> float:
    """
    Penalizes unsafe patches heavily.
    """

    if not is_allowed(patch):
        return -1.0  # instant disqualification

    return pre_score
