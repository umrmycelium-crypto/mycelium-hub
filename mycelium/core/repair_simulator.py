def simulate_patch(patch):
    """
    Fake execution environment.
    Never touches real registry or runtime.
    """

    # deterministic simulation rules
    if "system." in patch.target:
        return {
            "status": "safe",
            "risk": "low",
            "impact": "registry-level change"
        }

    return {
        "status": "unknown",
        "risk": "medium",
        "impact": "unclassified"
    }
