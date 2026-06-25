from mycelium.core.event_bus import EVENT_BUS
from mycelium.core.event_bus_tap import tap_event

_original_emit = EVENT_BUS.emit if hasattr(EVENT_BUS, "emit") else None


def patched_emit(event):
    tap_event(event)

    if _original_emit:
        return _original_emit(event)

    return None


EVENT_BUS.emit = patched_emit
