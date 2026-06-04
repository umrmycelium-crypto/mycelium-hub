from ..core.context import get_system_state, get_recent_events

def build_context():
    """
    Assembles a unified context object containing state and history.
    """
    state = get_system_state()
    events = get_recent_events(limit=5) # Limit for prompt efficiency

    return {
        "state": state,
        "recent_events": events
    }
