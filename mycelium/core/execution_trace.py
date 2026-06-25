from time import time

TRACE_BUFFER = []


def trace(event_type: str, data: dict):
    """
    Non-invasive execution tracer.
    """

    TRACE_BUFFER.append({
        "time": time(),
        "type": event_type,
        "data": data
    })

    # prevent unbounded growth
    if len(TRACE_BUFFER) > 500:
        del TRACE_BUFFER[:100]


def get_trace(limit: int = 50):
    return TRACE_BUFFER[-limit:]


def clear_trace():
    TRACE_BUFFER.clear()
    return {"status": "CLEARED"}


def system_trace(payload, context):
    return {
        "status": "OK",
        "trace": get_trace(payload.get("limit", 50))
    }
