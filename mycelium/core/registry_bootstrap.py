
from mycelium.core.proposal_ledger import list_proposals
from mycelium.core.capability_miner import mine_capabilities


def system_proposals(payload, context):
    return {
        "status": "OK",
        "proposals": list_proposals()
    }


def system_mine(payload, context):
    return mine_capabilities()


REGISTRY_BOOTSTRAP_EXTENSIONS = {
    "system.proposals": system_proposals,
    "system.mine": system_mine
}
