from mycelium.core.policy_sandbox import simulate_policy_change


def run_scenarios(changes_list):
    """
    Compare multiple hypothetical constitution mutations.
    """

    results = []

    for i, change in enumerate(changes_list):
        result = simulate_policy_change(change)
        result["scenario_id"] = i
        results.append(result)

    return {
        "scenarios": results
    }
