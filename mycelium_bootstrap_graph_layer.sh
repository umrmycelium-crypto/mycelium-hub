#!/bin/bash

set +e

echo "[Mycelium Graph Layer] injecting live system graph runtime"

# ─────────────────────────────────────────────
# 1. Add graph builder module
# ─────────────────────────────────────────────
cat > mycelium/runtime/live_graph.py << 'PY'
from mycelium.core.execution_trace import get_trace

def build_graph(trace):
    nodes = {}
    edges = {}

    # trace expected: list of events
    for event in trace:
        src = event.get("source", "unknown")
        dst = event.get("target", "dashboard")

        nodes[src] = nodes.get(src, 0) + 1
        nodes[dst] = nodes.get(dst, 0) + 1

        key = f"{src}->{dst}"
        edges[key] = edges.get(key, 0) + 1

    return {
        "nodes": [
            {"id": k, "weight": v}
            for k, v in nodes.items()
        ],
        "edges": [
            {"id": k, "weight": v}
            for k, v in edges.items()
        ],
        "heartbeat": {
            "total_events": len(trace),
            "active_nodes": len(nodes)
        }
    }
PY

# ─────────────────────────────────────────────
# 2. Patch dashboard server to stream graph
# ─────────────────────────────────────────────
cat > mycelium/runtime/dashboard_server.py << 'PY'
from fastapi import FastAPI, WebSocket
import asyncio

from mycelium.core.execution_trace import get_trace
from mycelium.runtime.ws_bridge import register_client, unregister_client
from mycelium.runtime.live_graph import build_graph

app = FastAPI()

@app.get("/")
def root():
    return {"status": "mycelium-live-graph"}

@app.websocket("/ws")
async def ws_endpoint(ws: WebSocket):
    await ws.accept()
    await register_client(ws)

    try:
        while True:
            await asyncio.sleep(0.5)

            trace = get_trace(30)
            graph = build_graph(trace)

            await ws.send_json({
                "type": "graph_update",
                "data": graph
            })

    except Exception:
        await unregister_client(ws)
PY

# ─────────────────────────────────────────────
# 3. restart clean
# ─────────────────────────────────────────────
pkill -f uvicorn || true
sleep 1

echo "[Mycelium Graph Layer] starting runtime..."

exec ./venv/bin/uvicorn mycelium.runtime.dashboard_server:app \
    --host 127.0.0.1 \
    --port 8081 \
    --reload
