import copy
import time

CONSTITUTION_HISTORY = []

CURRENT_CONSTITUTION = {
    "version": 1,
    "allow_self_modify_kernel": False,
    "allow_auto_registry_changes": False,
    "allow_policy_mutation": False,
    "min_confidence_to_execute": 0.75,
    "required_simulation": True
}


def get_constitution():
    return CURRENT_CONSTITUTION


def save_version(reason="manual_update"):
    snapshot = copy.deepcopy(CURRENT_CONSTITUTION)

    CONSTITUTION_HISTORY.append({
        "timestamp": time.time(),
        "reason": reason,
        "constitution": snapshot
    })

    return len(CONSTITUTION_HISTORY)


def history():
    return CONSTITUTION_HISTORY
