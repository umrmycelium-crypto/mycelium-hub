from mycelium.core.constitutional_consensus import resolve_consensus


def distributed_governance(patch, agent_votes):
    """
    Final authority is distributed, not local.
    """

    consensus = resolve_consensus(agent_votes)

    return {
        "allowed": consensus["approved"],
        "consensus": consensus,
        "mode": "distributed_constitution"
    }
