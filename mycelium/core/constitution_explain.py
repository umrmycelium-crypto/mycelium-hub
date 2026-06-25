from mycelium.core.constitution_store import get_constitution


def explain_decision(score, simulation_ok):
    constitution = get_constitution()

    reasons = []

    if score < constitution["min_confidence_to_execute"]:
        reasons.append(
            f"score below threshold ({constitution['min_confidence_to_execute']})"
        )

    if constitution["required_simulation"] and not simulation_ok:
        reasons.append(
            "simulation required but unavailable"
        )

    if not reasons:
        reasons.append("constitutional requirements satisfied")

    return {
        "constitution_version": constitution["version"],
        "reasons": reasons
    }
