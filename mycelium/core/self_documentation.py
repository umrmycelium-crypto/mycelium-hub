from mycelium.core.registry_core import get_registry
from mycelium.core.proposal_ledger import list_proposals


def generate_system_map():
    registry = get_registry()
    proposals = list_proposals()

    return {
        "system": {
            "registered_intents": list(registry.keys()),
            "registry_size": len(registry),
        },
        "evolution": {
            "pending_proposals": len(proposals),
            "high_confidence": [
                p for p in proposals if p.get("confidence", 0) > 0.7
            ]
        },
        "architecture": {
            "layers": [
                "intent_compiler",
                "router",
                "execution_layer",
                "proposal_engine",
                "consensus_engine",
                "commit_engine",
                "documentation_layer"
            ]
        }
    }


def system.self_map(payload, context):
    return generate_system_map()
