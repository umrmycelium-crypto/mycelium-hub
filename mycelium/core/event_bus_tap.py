from mycelium.runtime.live_graph import ingest_event

def tap_event(event: dict):
    try:
        ingest_event(event)
    except Exception:
        pass
