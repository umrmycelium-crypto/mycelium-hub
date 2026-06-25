from mycelium.core.repair_constitution_proposals import propose_change
from mycelium.core.repair_constitution_state import simulate_constitution_change
from mycelium.core.repair_constitution_voting import governance_vote
from mycelium.core.repair_constitution_evolution import apply_constitution_change, reject_proposal


def constitutional_evolution(rule_key, new_value, reason):
    proposal = propose_change(rule_key, new_value, reason)

    simulation = simulate_constitution_change(rule_key, new_value)

    vote = governance_vote(simulation, proposal)

    decision = {
        "proposal": proposal,
        "simulation": simulation,
        "vote": vote
    }

    if vote["approved"]:
        decision["result"] = apply_constitution_change(proposal)
        decision["executed"] = True
    else:
        decision["result"] = reject_proposal(proposal)
        decision["executed"] = False

    return decision
