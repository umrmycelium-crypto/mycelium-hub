from mycelium.core.governance_events import get_events


def build_timeline(limit=200):
    events = get_events()[-limit:]

    timeline = []

    for e in events:
        timeline.append({
            "time": e["timestamp"],
            "type": e["event"],
            "summary": summarize_event(e)
        })

    return timeline


def summarize_event(event):
    data = event.get("data", {})

    if event["event"] == "proposal_received":
        return f"proposal {data.get('proposal_id')} received"

    if event["event"] == "simulation_complete":
        return "simulation executed"

    if event["event"] == "validation_complete":
        return "validation completed"

    if event["event"] == "agent_approval":
        return f"agent approval: {data.get('approved')}"

    if event["event"] == "human_review_requested":
        return f"human review requested: {data.get('request_id')}"

    if event["event"] == "mutation_committed":
        return "mutation committed"

    if event["event"] == "pipeline_rejected":
        return f"pipeline rejected at {data.get('stage')}"

    return str(data)
