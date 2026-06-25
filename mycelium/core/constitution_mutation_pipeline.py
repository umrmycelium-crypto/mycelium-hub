from mycelium.core.constitution_mutation import get_proposal
from mycelium.core.constitution_mutation_simulator import simulate_mutation
from mycelium.core.constitution_mutation_validator import validate_mutation
from mycelium.core.constitution_mutation_approver import approve_mutation
from mycelium.core.constitution_mutation_commit import commit_mutation
from mycelium.core.constitution_store import get_constitution

from mycelium.core.constitution_human_override import create_review_request
from mycelium.core.governance_events import emit_event


def run_mutation_pipeline(proposal_id: str, require_human=True):
    proposal = get_proposal(proposal_id)

    if not proposal:
        return {"status": "error", "reason": "proposal_not_found"}

    change = proposal["change"]

    emit_event("proposal_received", {"proposal_id": proposal_id})

    simulation = simulate_mutation(change)
    emit_event("simulation_complete", simulation)

    validation = validate_mutation(change)
    emit_event("validation_complete", validation)

    constitution = get_constitution()

    agent_ok = approve_mutation(simulation, validation, constitution)
    emit_event("agent_approval", {"approved": agent_ok})

    if not agent_ok:
        emit_event("pipeline_rejected", {"stage": "agent"})
        return {
            "status": "rejected_agent",
            "simulation": simulation,
            "validation": validation
        }

    if require_human:
        request_id = create_review_request(proposal_id, simulation, validation)
        emit_event("human_review_requested", {"request_id": request_id})

        return {
            "status": "awaiting_human",
            "request_id": request_id,
            "proposal_id": proposal_id
        }

    result = commit_mutation(change, proposal_id)
    emit_event("mutation_committed", result)

    return result
