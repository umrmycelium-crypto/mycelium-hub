#!/bin/bash

set +e

PORT=${1:-8081}

echo "[Mycelium Bootstrap FINAL FIX] Starting on port $PORT"

pkill -f uvicorn || true
sleep 1

# ─────────────────────────────────────────────
# 1. Ensure ws_bridge exports correct API
# ─────────────────────────────────────────────
echo "[1/5] Rebuilding ws_bridge API surface..."

cat > mycelium/runtime/ws_bridge.py << 'PY'
clients = set()

async def register_client(ws):
    clients.add(ws)

async def unregister_client(ws):
    clients.discard(ws)

async def broadcast(message):
    dead = []

    for ws in list(clients):
        try:
            await ws.send_json(message)
        except Exception:
            dead.append(ws)

    for ws in dead:
        clients.discard(ws)
PY

# ─────────────────────────────────────────────
# 2. Fix dashboard imports (explicit + safe)
# ─────────────────────────────────────────────
echo "[2/5] Fixing dashboard imports..."

cat > mycelium/runtime/dashboard_server.py << 'PY'
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
PY

# ─────────────────────────────────────────────
# 3. Ensure websocket deps
# ─────────────────────────────────────────────
echo "[3/5] Ensuring dependencies..."
./venv/bin/pip install -q "uvicorn[standard]" websockets fastapi

# ─────────────────────────────────────────────
# 4. Clean restart
# ─────────────────────────────────────────────
echo "[4/5] Restarting system..."
exec ./venv/bin/uvicorn mycelium.runtime.dashboard_server:app \
    --host 127.0.0.1 \
    --port "$PORT" \
    --reload
