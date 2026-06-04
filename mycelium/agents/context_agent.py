from ..core.context import get_system_state, get_recent_events
from ..memory.manager import load_memory

def build_context():
    """
    Assembles a unified context object containing state, history, and persistent memory.
    """
    state = get_system_state()
    events = get_recent_events(limit=5)
    memory = load_memory()

    return {
        "state": state,
        "recent_events": events,
        "memory": memory
    }
