import copy
from mycelium.core.registry_core import get_registry

REGISTRY_HISTORY = []


def snapshot_registry():
    reg = get_registry()
    REGISTRY_HISTORY.append(copy.deepcopy(reg))
    return len(REGISTRY_HISTORY) - 1


def rollback(version: int):
    reg = get_registry()
    old = REGISTRY_HISTORY[version]

    reg.clear()
    reg.update(old)

    return {
        "status": "ROLLED_BACK",
        "version": version
    }


def commit_proposal(proposal, registry):
    """
    Only safe install point in system.
    """

    snapshot_registry()

    name = proposal["name"]
    handler = proposal.get("handler")

    if callable(handler):
        registry[name] = handler
    else:
        # placeholder handler
        def generated_handler(payload, context):
            return {
                "status": "AUTO_GENERATED",
                "name": name,
                "payload": payload
            }

        registry[name] = generated_handler

    return {
        "status": "COMMITTED",
        "name": name
    }
