from mycelium.core.policy_sandbox import simulate_policy_change
from mycelium.core.policy_safety_score import compute_safety_score


def analyze_change(change: dict):
    result = simulate_policy_change(change)

    score = compute_safety_score(result["risk_analysis"])

    return {
        "simulation": result,
        "safety_score": score,
        "recommendation": (
            "ALLOW" if score > 70 else
            "REVIEW" if score > 40 else
            "REJECT"
        )
    }
