from mycelium.core.governance_events import get_events
from mycelium.core.governance_causal_engine import CAUSAL_CHAIN_RULES


def trace_root_cause(target_event_type):
    events = get_events()

    target_indexes = [
        i for i, e in enumerate(events)
        if e["event"] == target_event_type
    ]

    chains = []

    for t in target_indexes:
        chain = []

        for i in range(t - 1, -1, -1):
            prev = events[i]["event"]
            current = events[i + 1]["event"]

            if (prev, current) in CAUSAL_CHAIN_RULES:
                chain.insert(0, events[i])
                chain.append(events[i + 1])

        chains.append(chain)

    return {
        "target": target_event_type,
        "causal_chains": chains
    }
