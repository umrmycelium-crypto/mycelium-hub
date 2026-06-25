from collections import defaultdict
import time

from mycelium.core.governance_events import get_events


def detect_anomalies(window_seconds=3600):
    """
    Detect governance irregularities over recent time window.
    """

    now = time.time()
    events = get_events()

    recent = [
        e for e in events
        if now - e["timestamp"] <= window_seconds
    ]

    counts = defaultdict(int)

    for e in recent:
        counts[e["event"]] += 1

    anomalies = []

    # ----------------------------------
    # RULE 1: excessive mutations
    # ----------------------------------
    mutation_events = counts.get("mutation_committed", 0)

    if mutation_events > 10:
        anomalies.append({
            "type": "mutation_spike",
            "severity": "HIGH",
            "value": mutation_events
        })

    # ----------------------------------
    # RULE 2: high rejection rate
    # ----------------------------------
    rejected = counts.get("pipeline_rejected", 0)

    if rejected > 5:
        anomalies.append({
            "type": "high_rejection_rate",
            "severity": "MEDIUM",
            "value": rejected
        })

    # ----------------------------------
    # RULE 3: excessive human gating
    # ----------------------------------
    human_requests = counts.get("human_review_requested", 0)

    if human_requests > 15:
        anomalies.append({
            "type": "human_overload",
            "severity": "MEDIUM",
            "value": human_requests
        })

    # ----------------------------------
    # RULE 4: simulation instability
    # ----------------------------------
    sim_events = counts.get("simulation_complete", 0)

    if sim_events > 20:
        anomalies.append({
            "type": "simulation_pressure",
            "severity": "LOW",
            "value": sim_events
        })

    return {
        "window_seconds": window_seconds,
        "event_counts": dict(counts),
        "anomalies": anomalies,
        "status": "complete"
    }
