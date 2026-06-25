from mycelium.core.repair_constitution import CONSTITUTION


def simulate_constitution_change(rule_key, new_value):
    """
    Dry-run constitution mutation.
    """

    simulated = CONSTITUTION.copy()
    simulated[rule_key] = new_value

    risk = "low"

    # simple safety heuristics
    if "allow_self" in rule_key and new_value is True:
        risk = "high"

    if "min_confidence" in rule_key and new_value < 0.5:
        risk = "high"

    return {
        "simulated_constitution": simulated,
        "risk": risk,
        "impact": "system-wide governance change"
    }
