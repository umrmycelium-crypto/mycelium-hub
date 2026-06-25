import copy

from mycelium.core.constitution_store import get_constitution
from mycelium.core.constitution_diff_engine import diff_constitutions
from mycelium.core.constitution_diff_classifier import classify_diff


def simulate_policy_change(change: dict):
    """
    Run a safe, non-destructive simulation of a constitution mutation.
    """

    current = get_constitution()
    simulated = copy.deepcopy(current)

    simulated.update(change)

    diff = diff_constitutions(current, simulated)
    classification = classify_diff(diff)

    return {
        "base_constitution": current,
        "simulated_constitution": simulated,
        "diff": diff,
        "risk_analysis": classification,
        "status": "simulation_complete"
    }
