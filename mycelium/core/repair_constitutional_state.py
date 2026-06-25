from mycelium.core.repair_constitution import CONSTITUTION

"""
Split constitution into immutable + evolving layers
"""

IMMUTABLE_CONSTITUTION = CONSTITUTION.copy()

# runtime-evolving layer
ACTIVE_AMENDMENTS = []

def get_full_constitution():
    return IMMUTABLE_CONSTITUTION + ACTIVE_AMENDMENTS


def get_immutable():
    return IMMUTABLE_CONSTITUTION


def get_amendments():
    return ACTIVE_AMENDMENTS
