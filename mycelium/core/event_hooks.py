from mycelium.core.event_bus import EVENT_BUS
from mycelium.runtime.ws_bridge import broadcast


def emit(event_type: str, payload: dict):
    event = {
        "type": event_type,
        "payload": payload
    }

    # core system bus
    try:
        EVENT_BUS.emit(event_type, payload)
    except Exception:
        pass

    # live UI stream
    try:
        import asyncio
        asyncio.create_task(broadcast(event))
    except Exception:
        pass
