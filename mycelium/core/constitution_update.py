from mycelium.core.constitution_store import (
    CURRENT_CONSTITUTION,
    save_version
)


def update_constitution(changes: dict, reason="approved_change"):
    save_version(reason)

    CURRENT_CONSTITUTION.update(changes)

    CURRENT_CONSTITUTION["version"] += 1

    return CURRENT_CONSTITUTION
