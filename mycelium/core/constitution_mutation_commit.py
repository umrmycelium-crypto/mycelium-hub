from mycelium.core.constitution_store import (
    CURRENT_CONSTITUTION,
    save_version
)


def commit_mutation(change: dict, proposal_id: str):
    """
    Apply approved mutation safely.
    """

    save_version(reason=f"mutation:{proposal_id}")

    CURRENT_CONSTITUTION.update(change)

    CURRENT_CONSTITUTION["version"] += 1

    return {
        "status": "committed",
        "version": CURRENT_CONSTITUTION["version"]
    }
