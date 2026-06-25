from mycelium.core.proposal_ledger import list_proposals


def visualize_proposals():
    proposals = list_proposals()

    return {
        "total": len(proposals),
        "pending": [p for p in proposals if p.get("status") == "proposed"],
        "approved": [p for p in proposals if p.get("status") == "approved"]
    }


def system_evolution_view(payload, context):
    return visualize_proposals()
