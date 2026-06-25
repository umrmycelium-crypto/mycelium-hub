def approve_mutation(simulation, validation, constitution):
    """
    Final approval gate before commit.
    """

    if not validation[0]:
        return False

    if simulation["risk"] == "high":
        return False

    if constitution.get("required_simulation") and not simulation:
        return False

    return True
