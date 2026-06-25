"""
Repair Constitution v1
Hard safety + evolution constraints
"""

CONSTITUTION = {
    "allow_self_modify_kernel": False,
    "allow_auto_registry_changes": False,
    "allow_policy_mutation": False,

    "max_patch_risk": "low",

    "required_simulation": True,

    "min_confidence_to_execute": 0.75,

    "allowed_intents": [
        "system.ping",
        "system.status",
        "system.repair.analyze",
        "system.repair.loop",
        "system.repair.multi",
        "ai.ask",
        "media.play"
    ]
}


def check_constitution(patch, simulation, score):
    """
    Final constitutional gate.
    """

    if not CONSTITUTION["required_simulation"] and simulation:
        return False

    if score < CONSTITUTION["min_confidence_to_execute"]:
        return False

    if simulation.get("risk") not in ["low"]:
        return False

    if patch.target not in CONSTITUTION["allowed_intents"]:
        return False

    return True
