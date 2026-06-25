import time

EVENT_LOG = []


def emit_event(event_type, data):
    EVENT_LOG.append({
        "timestamp": time.time(),
        "event": event_type,
        "data": data
    })


def get_events():
    return EVENT_LOG


def clear_events():
    EVENT_LOG.clear()


from mycelium.core.governance_memory_builder import build_memory_from_event


_original_emit = emit_event


def emit_event(event_type, data):
    event = {
        "timestamp": time.time(),
        "event": event_type,
        "data": data
    }

    EVENT_LOG.append(event)

    # semantic memory hook
    try:
        build_memory_from_event(event)
    except Exception:
        pass

from mycelium.core.governance_telemetry import publish


def emit_event(event_type, data):
    event = {
        "timestamp": time.time(),
        "event": event_type,
        "data": data
    }

    EVENT_LOG.append(event)

    # 🔴 LIVE TELEMETRY HOOK
    publish("events", event)

    return event
