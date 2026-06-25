#!/bin/bash
set -e

echo "[Mycelium Self-Perception Layer] constructing introspective graph"

./venv/bin/pip install -q networkx

# 1. Replace execution_trace interpretation layer
cat > mycelium/core/graph_introspector.py << 'PY'
from mycelium.core.execution_trace import get_trace
from collections import defaultdict

def build_self_graph(limit=200):
    trace = get_trace(limit)

    nodes = defaultdict(int)
    edges = defaultdict(int)

    for event in trace:
        src = event.get("module", "unknown")
        dst = event.get("target", "system")

        nodes[src] += 1
        edges[(src, dst)] += 1

    return {
        "nodes": [
            {"id": n, "weight": w}
            for n, w in nodes.items()
        ],
        "edges": [
            {"source": a, "target": b, "weight": w}
            for (a, b), w in edges.items()
        ]
    }
PY

# 2. Extend ws_bridge into self-model broadcaster
cat > mycelium/runtime/ws_bridge.py << 'PY'
import asyncio
from mycelium.core.execution_trace import get_trace
from mycelium.core.graph_introspector import build_self_graph

clients = set()

async def register_client(ws):
    clients.add(ws)

async def unregister_client(ws):
    clients.discard(ws)

async def broadcast():
    while True:
        await asyncio.sleep(0.5)

        graph = build_self_graph(200)

        payload = {
            "pulse": len(get_trace(50)),
            "graph": graph
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

# 3. Patch frontend into graph renderer (self-aware visualization)
cat > mycelium/runtime/static/index.html << 'HTML'
<!DOCTYPE html>
<html>
<head>
  <title>Mycelium Self-Perception Graph</title>
  <style>
    body { margin:0; background:#04060a; overflow:hidden; font-family: monospace; }
    canvas { width:100vw; height:100vh; display:block; }
    #hud { position:absolute; top:10px; left:10px; color:#7fffd4; }
  </style>
</head>
<body>
<canvas id="c"></canvas>
<div id="hud">Mycelium Self-Perception Layer • introspecting system graph</div>

<script>
const c = document.getElementById("c");
const ctx = c.getContext("2d");

let graph = {nodes:[], edges:[]};

const ws = new WebSocket("ws://" + location.host + "/ws");

ws.onmessage = (e) => {
  const data = JSON.parse(e.data);
  graph = data.graph || graph;
};

function draw(){
  ctx.fillStyle = "rgba(4,6,10,0.35)";
  ctx.fillRect(0,0,c.width,c.height);

  const nodes = graph.nodes;

  for (let i=0;i<nodes.length;i++){
    const n = nodes[i];

    const x = (i * 97) % c.width;
    const y = (i * 193) % c.height;

    const r = 2 + (n.weight * 0.2);

    ctx.beginPath();
    ctx.arc(x,y,r,0,Math.PI*2);
    ctx.fillStyle = "#7fffd4";
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

echo "[Mycelium Self-Perception Layer] complete"
echo "Restart: ./run_dashboard.sh 8081"
