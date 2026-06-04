from .event_bus import EventBus
from .. import actions
from ..subscribers.logger import handle_log

def register_all():
    """
    Initializes the global event bus and registers all standard Mycelium handlers.
    """
    bus = EventBus()

    # Core Intent Mappings
    bus.subscribe("media.play", actions.handle_media_play)
    bus.subscribe("media.search", actions.handle_media_search)
    bus.subscribe("media.status", actions.handle_media_status)
    bus.subscribe("system.status", actions.handle_system_status)
    bus.subscribe("knowledge.search", actions.handle_knowledge_search)
    bus.subscribe("developer.assist", actions.handle_dev_assist)
    bus.subscribe("media.request_download", actions.handle_media_request)
    bus.subscribe("unknown", actions.handle_unknown)

    # Global Observability
    bus.subscribe("*", handle_log)

    return bus
