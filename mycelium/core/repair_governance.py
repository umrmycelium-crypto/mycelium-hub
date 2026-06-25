from mycelium.core.repair_constitution import check_constitution


def govern_repair(patch, simulation, score):
    """
    Final authority gate (cannot be bypassed)
    """

    allowed = check_constitution(patch, simulation, score)

    return {
        "allowed": allowed,
        "reason": "constitutional_gate"
    }
