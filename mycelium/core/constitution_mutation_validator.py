from mycelium.core.constitution_store import CURRENT_CONSTITUTION


def validate_mutation(change: dict):
    """
    Ensure mutation does not violate hard constraints.
    """

    if "allow_self_modify_kernel" in change:
        return False, "kernel self-modification forbidden"

    if "allow_auto_registry_changes" in change:
        return False, "auto registry mutation forbidden"

    return True, "ok"
