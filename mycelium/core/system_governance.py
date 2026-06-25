from mycelium.core.invariants import INVARIANTS


def system_governance(payload=None, context=None):
    """
    Returns current system governance rules.
    """

    return {
        "status": "OK",
        "invariants": INVARIANTS,
        "count": len(INVARIANTS)
    }
