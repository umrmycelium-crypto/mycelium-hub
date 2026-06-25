from mycelium.core.proposal_ledger import submit_proposal


AGENTS = {
    "observer": {"role": "analysis"},
    "executor": {"role": "execution"},
    "governor": {"role": "policy"},
}


def agent_propose(agent_name: str, proposal: dict):
    return submit_proposal({
        **proposal,
        "author": agent_name
    })


def swarm_consensus(proposal: dict):
    """
    Simple distributed vote simulation.
    """

    votes = {
        "observer": True,
        "executor": proposal.get("risk") != "high",
        "governor": proposal.get("confidence", 0) > 0.6
    }

    return {
        "approved": all(votes.values()),
        "votes": votes
    }


def system_swarm_status(payload, context):
    return {
        "agents": list(AGENTS.keys())
    }
