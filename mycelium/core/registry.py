from .event_bus import EventBus
from .. import actions

def register_all():
    """
    Initializes the global event bus and registers all standard Mycelium handlers.
    """
    bus = EventBus()

    # Core Intent Mappings
    bus.subscribe("media.play", actions.handle_media_play)
    bus.subscribe("media.search", actions.handle_media_search)
    bus.subscribe("system.status", actions.handle_system_status)
    bus.subscribe("knowledge.search", actions.handle_knowledge_search)
    bus.subscribe("developer.assist", actions.handle_dev_assist)
    bus.subscribe("unknown", actions.handle_unknown)

    return bus
