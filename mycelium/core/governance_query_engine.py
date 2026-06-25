from mycelium.core.governance_events import get_events


def run_query(parsed):
    events = get_events()

    t = parsed["type"]

    if t == "rollback":
        return [e for e in events if "rollback" in e["event"]]

    if t == "human_events":
        return [e for e in events if "human" in e["event"]]

    if t == "risk_events":
        return [e for e in events if e["event"] in [
            "pipeline_rejected",
            "validation_complete"
        ]]

    if t == "simulation":
        return [e for e in events if e["event"] == "simulation_complete"]

    if t == "drift":
        return [e for e in events if e["event"] in [
            "mutation_committed",
            "pipeline_rejected"
        ]]

    return []
