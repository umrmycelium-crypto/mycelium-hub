from mycelium.core.governance_events import get_events


def replay_events():
    return get_events()


def replay_by_type(event_type):
    return [
        e for e in get_events()
        if e["event"] == event_type
    ]


def explain_pipeline(proposal_id):
    events = get_events()

    filtered = [
        e for e in events
        if proposal_id in str(e["data"])
    ]

    return {
        "proposal_id": proposal_id,
        "timeline": filtered
    }
