from fastapi import FastAPI
from mycelium.core.execution_trace import get_trace
from mycelium.core.registry_core import get_registry
from mycelium.core.event_store_db import read_events

app = FastAPI()


@app.get("/")
def home():
    return {"status": "Mycelium UI online"}


@app.get("/state")
def state():
    return {
        "registry": list(get_registry().keys()),
        "trace_size": len(get_trace(200)),
        "events": len(read_events(1000))
    }


@app.get("/trace")
def trace():
    return get_trace(200)


@app.get("/events")
def events():
    return read_events(100)
