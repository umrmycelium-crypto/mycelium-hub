def allow_patch(patch, simulation_result):
    """
    Hard safety constraints.
    """

    blocked_targets = [
        "system.kernel",
        "registry_core",
        "auth",
        "node_identity"
    ]

    if any(b in patch.target for b in blocked_targets):
        return False

    if simulation_result.get("risk") == "high":
        return False

    return True
