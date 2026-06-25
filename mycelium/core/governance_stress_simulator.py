import random
import time

from mycelium.core.governance_events import emit_event


EVENT_FLOW = [
    "proposal_received",
    "simulation_complete",
    "validation_complete",
    "agent_approval",
    "human_review_requested",
    "mutation_committed",
    "pipeline_rejected",
    "rollback_triggered"
]


def run_stress_simulation(cycles=20, delay=0.01):
    """
    Synthetic governance stress test.
    Generates realistic event chains.
    """

    results = []

    for i in range(cycles):
        proposal_id = f"p-{i}"

        sequence = random.choices(
            EVENT_FLOW,
            weights=[10, 10, 10, 8, 5, 7, 4, 3],
            k=random.randint(4, 7)
        )

        for event in sequence:
            payload = {
                "proposal_id": proposal_id,
                "cycle": i,
                "event_index": sequence.index(event)
            }

            emit_event(event, payload)

            results.append({
                "event": event,
                "proposal_id": proposal_id
            })

            time.sleep(delay)

    return {
        "status": "complete",
        "cycles": cycles,
        "events_emitted": len(results)
    }
