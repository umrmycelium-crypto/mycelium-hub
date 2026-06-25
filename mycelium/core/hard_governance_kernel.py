REQUIRED_INVARIANTS = {
    "no_direct_vault_access": True,
    "no_registry_mutation_outside_commit": True,
    "no_unauthorized_intent_execution": True
}


def validate_execution(intent: dict):
    """
    Hard gate before ANY execution.
    """

    name = intent.get("name")

    if not name:
        return {"allowed": False, "reason": "missing intent name"}

    if "vault" in name and name != "system.vault.status":
        return {"allowed": False, "reason": "vault access restricted"}

    if "registry" in name and name != "system.repair.status":
        return {"allowed": False, "reason": "registry mutation forbidden here"}

    return {"allowed": True}


def system_governance_check(payload, context):
    return validate_execution(payload)
