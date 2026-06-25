from fastapi import FastAPI, Request
import uvicorn
from mycelium.core.router import route
from mycelium.core.event_store import append_event

app = FastAPI()


@app.post("/execute")
async def execute(request: Request):
    intent = await request.json()

    # log inbound event (source of truth)
    append_event({
        "event": "rpc.intent",
        "payload": intent
    })

    result = route(intent)

    append_event({
        "event": "rpc.result",
        "payload": result
    })

    return result


@app.get("/health")
def health():
    return {"status": "OK"}


def run(port: int = 8000):
    uvicorn.run(app, host="0.0.0.0", port=port)
