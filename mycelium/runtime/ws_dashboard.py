from fastapi import FastAPI, WebSocket
import asyncio

from mycelium.runtime.ws_bridge import register_client, unregister_client, broadcast
from mycelium.core.execution_trace import get_trace

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    register_client(ws)

    try:
        while True:
            # reactive snapshot = system "self-perception"
            snapshot = {
                "type": "live.graph",
                "trace": get_trace(30),
                "status": "ALIVE"
            }

            await broadcast(snapshot)
            await asyncio.sleep(0.5)

    finally:
        unregister_client(ws)
