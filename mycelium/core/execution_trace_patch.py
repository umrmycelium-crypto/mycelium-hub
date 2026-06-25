from mycelium.core.execution_trace import TRACE
from mycelium.core.event_hooks import emit


def record(event_type: str, payload: dict):
    TRACE.append({
        "type": event_type,
        "payload": payload
    })

    emit("trace.event", {
        "type": event_type
    })
