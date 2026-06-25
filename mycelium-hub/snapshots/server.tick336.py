from fastapi import FastAPI, WebSocket
import asyncio

app = FastAPI()

class Runtime:
    def __init__(self):
        self.tick = 0
        self.nodes = {
            "seed": 0.5,
            "memory": 0.2,
            "intent": 0.7
        }

    def step(self):
        self.tick += 1

        # smooth decay + drift
        for k in self.nodes:
            self.nodes[k] *= 0.98

        self.nodes["intent"] += 0.005

        return {
            "tick": self.tick,
            "nodes": self.nodes
        }

runtime = Runtime()

@app.get("/tick")
def tick():
    return runtime.step()

@app.websocket("/ws")
async def ws(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            state = runtime.step()
            await websocket.send_json({
                "type": "tick",
                "payload": state
            })
            await asyncio.sleep(1)

    except Exception:
        # silently close broken connections
        return
