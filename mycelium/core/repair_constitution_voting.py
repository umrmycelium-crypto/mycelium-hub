def governance_vote(simulation, proposal):
    """
    Deterministic governance decision layer.
    """

    risk = simulation.get("risk")

    if risk == "high":
        return {
            "approved": False,
            "reason": "risk_too_high"
        }

    if "self_modify" in proposal["rule"]:
        return {
            "approved": False,
            "reason": "violates_core_constraint"
        }

    return {
        "approved": True,
        "reason": "within_safe_bounds"
    }
