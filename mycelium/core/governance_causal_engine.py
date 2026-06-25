from mycelium.core.governance_events import get_events


CAUSAL_CHAIN_RULES = [
    ("proposal_received", "simulation_complete"),
    ("simulation_complete", "validation_complete"),
    ("validation_complete", "agent_approval"),
    ("agent_approval", "human_review_requested"),
    ("human_review_requested", "mutation_committed"),
    ("validation_complete", "pipeline_rejected"),
]


def build_causal_links(limit=300):
    events = get_events()[-limit:]

    links = []

    for i, e in enumerate(events):
        for j in range(i + 1, len(events)):
            a = e["event"]
            b = events[j]["event"]

            if (a, b) in CAUSAL_CHAIN_RULES:
                links.append({
                    "cause": i,
                    "effect": j,
                    "cause_type": a,
                    "effect_type": b
                })

    return {
        "links": links,
        "total": len(links)
    }
