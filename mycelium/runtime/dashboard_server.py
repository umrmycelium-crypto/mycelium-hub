from fastapi import FastAPI, WebSocket
from mycelium.core.execution_trace import get_trace
from mycelium.runtime.ws_bridge import register_client, unregister_client, broadcast
import asyncio

app = FastAPI()

@app.get("/")
def home():
    return {"status": "mycelium-live"}

@app.websocket("/ws")
async def ws_endpoint(ws: WebSocket):
    await ws.accept()
    await register_client(ws)

    try:
        while True:
            await asyncio.sleep(0.5)
            await ws.send_json({
                "trace": get_trace(20),
                "status": "LIVE"
            })

    except Exception:
        await unregister_client(ws)
