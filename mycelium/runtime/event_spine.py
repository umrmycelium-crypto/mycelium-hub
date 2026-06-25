from mycelium.core.event_bus import EVENT_BUS
from mycelium.runtime.ws_bridge import broadcast

import asyncio


def install_event_spine():
    """
    Attaches a passive listener to EVENT_BUS.
    This does NOT modify event_bus behavior.
    It mirrors events into the reactive system graph.
    """

    original_emit = EVENT_BUS.emit if hasattr(EVENT_BUS, "emit") else None

    if not original_emit:
        return


    def wrapped_emit(event_type, payload=None, *args, **kwargs):
        result = original_emit(event_type, payload, *args, **kwargs)

        try:
            asyncio.create_task(
                broadcast({
                    "type": "event_bus.event",
                    "event": event_type,
                    "payload": payload
                })
            )
        except Exception:
            pass

        return result


    EVENT_BUS.emit = wrapped_emit
