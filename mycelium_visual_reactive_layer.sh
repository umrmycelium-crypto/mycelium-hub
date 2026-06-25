#!/bin/bash
set -e

echo "[Mycelium Reactive Layer] wiring live event brain"

# 1. Ensure websocket support
./venv/bin/pip install -q "uvicorn[standard]" websockets

# 2. Create reactive WS bridge (single source of truth)
cat > mycelium/runtime/ws_bridge.py << 'PY'
import asyncio
from mycelium.core.execution_trace import get_trace

clients = set()

async def register_client(ws):
    clients.add(ws)

async def unregister_client(ws):
    clients.discard(ws)

async def broadcast():
    while True:
        await asyncio.sleep(0.5)

        payload = {
            "trace": get_trace(20),
            "pulse": len(get_trace(20))
        }

        dead = []
        for c in clients:
            try:
                await c.send_json(payload)
            except:
                dead.append(c)

        for d in dead:
            clients.discard(d)
PY

# 3. Patch dashboard server into REAL reactive mode
cat > mycelium/runtime/dashboard_server.py << 'PY'
from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
import asyncio

from mycelium.runtime.ws_bridge import register_client, unregister_client, broadcast

app = FastAPI()

app.mount("/", StaticFiles(directory="mycelium/runtime/static", html=True), name="static")

@app.on_event("startup")
async def startup():
    asyncio.create_task(broadcast())

@app.websocket("/ws")
async def ws_endpoint(ws: WebSocket):
    await ws.accept()
    await register_client(ws)
    try:
        while True:
            await ws.receive_text()
    except:
        await unregister_client(ws)
PY

# 4. Upgrade frontend to REAL reactive rendering
cat > mycelium/runtime/static/index.html << 'HTML'
<!DOCTYPE html>
<html>
<head>
  <title>Mycelium Reactive Graph</title>
  <style>
    body { margin:0; background:#05070a; overflow:hidden; font-family: monospace; }
    canvas { width:100vw; height:100vh; display:block; }
    #hud { position:absolute; top:10px; left:10px; color:#7fffd4; opacity:0.8; }
  </style>
</head>
<body>
<canvas id="c"></canvas>
<div id="hud">Mycelium Reactive Graph • live trace feed</div>

<script>
const c = document.getElementById("c");
const ctx = c.getContext("2d");

let pulse = 1;
let nodes = Array.from({length: 60}, () => ({
  x: Math.random()*window.innerWidth,
  y: Math.random()*window.innerHeight,
  v: Math.random()*1.2 + 0.2
}));

const ws = new WebSocket("ws://" + location.host + "/ws");

ws.onmessage = (e) => {
  const data = JSON.parse(e.data);
  pulse = (data.pulse || 1);
};

function draw(t){
  ctx.fillStyle = "rgba(5,7,10,0.25)";
  ctx.fillRect(0,0,c.width,c.height);

  for (let n of nodes){
    const intensity = Math.min(5, pulse * 0.2);

    n.x += Math.sin(t*0.001 + n.y*0.01) * n.v * intensity;
    n.y += Math.cos(t*0.001 + n.x*0.01) * n.v * intensity;

    ctx.beginPath();
    ctx.arc(n.x,n.y,2 + intensity,0,Math.PI*2);
    ctx.fillStyle = `rgba(127,255,212,${0.3 + intensity*0.1})`;
    ctx.fill();
  }

  requestAnimationFrame(draw);
}

function resize(){
  c.width = window.innerWidth;
  c.height = window.innerHeight;
}
window.onresize = resize;
resize();

requestAnimationFrame(draw);
</script>
</body>
</html>
HTML

echo "[Mycelium Reactive Layer] complete"
echo "Restart: ./run_dashboard.sh 8081"
