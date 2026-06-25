import copy

from mycelium.core.constitution_store import (
    CONSTITUTION_HISTORY,
    CURRENT_CONSTITUTION
)


def rollback(version_index: int):
    if version_index < 0:
        raise ValueError("invalid version")

    if version_index >= len(CONSTITUTION_HISTORY):
        raise ValueError("version does not exist")

    snapshot = copy.deepcopy(
        CONSTITUTION_HISTORY[version_index]["constitution"]
    )

    CURRENT_CONSTITUTION.clear()
    CURRENT_CONSTITUTION.update(snapshot)

    return CURRENT_CONSTITUTION
