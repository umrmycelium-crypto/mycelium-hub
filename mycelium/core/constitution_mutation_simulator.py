from mycelium.core.constitution_store import CURRENT_CONSTITUTION


def simulate_mutation(change: dict):
    """
    Predict impact of a constitutional change.
    """

    simulated = CURRENT_CONSTITUTION.copy()
    simulated.update(change)

    risk_flags = []

    if simulated.get("allow_self_modify_kernel", False):
        risk_flags.append("kernel_self_modification_enabled")

    if simulated.get("min_confidence_to_execute", 0) < 0.5:
        risk_flags.append("low_execution_confidence")

    risk = "high" if risk_flags else "low"

    return {
        "resulting_constitution": simulated,
        "risk": risk,
        "flags": risk_flags
    }
