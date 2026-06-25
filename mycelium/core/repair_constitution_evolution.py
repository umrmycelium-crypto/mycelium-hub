from mycelium.core.repair_constitution import CONSTITUTION
from mycelium.core.repair_constitution_proposals import PROPOSALS


def apply_constitution_change(proposal):
    rule = proposal["rule"]
    value = proposal["new_value"]

    CONSTITUTION[rule] = value
    proposal["status"] = "applied"

    return {
        "status": "applied",
        "rule": rule,
        "value": value
    }


def reject_proposal(proposal):
    proposal["status"] = "rejected"
    return {"status": "rejected", "id": proposal["id"]}
