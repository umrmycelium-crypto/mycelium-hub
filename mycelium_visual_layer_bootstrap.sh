#!/bin/bash
set -e

PORT=${1:-8081}

echo "[Mycelium Visual Layer] stabilizing runtime on port $PORT"

# 1. Ensure websocket + uvicorn extras (fixes WS warning)
./venv/bin/pip install -q "uvicorn[standard]" websockets

# 2. Ensure static UI directory exists
mkdir -p mycelium/runtime/static

# 3. Create favicon (silent safe default)
cat > mycelium/runtime/static/favicon.ico << 'FAV'
FAV

# 4. Create minimal reactive graph UI (heartbeat canvas)
cat > mycelium/runtime/static/index.html << 'HTML'
<!DOCTYPE html>
<html>
<head>
  <title>Mycelium Live Graph</title>
  <style>
    body { margin:0; background:#05070a; color:#9ff; font-family: monospace; overflow:hidden; }
    #c { width:100vw; height:100vh; display:block; }
    #hud { position:absolute; top:10px; left:10px; opacity:0.7; }
  </style>
</head>
<body>
<canvas id="c"></canvas>
<div id="hud">Mycelium Live Graph • heartbeat active</div>

<script>
const c = document.getElementById("c");
const ctx = c.getContext("2d");

let nodes = Array.from({length: 40}, (_,i)=>({
  x: Math.random()*window.innerWidth,
  y: Math.random()*window.innerHeight,
  v: Math.random()*0.5+0.2
}));

function resize(){
  c.width = window.innerWidth;
  c.height = window.innerHeight;
}
window.onresize = resize;
resize();

function pulse(t){
  ctx.fillStyle = "rgba(5,7,10,0.25)";
  ctx.fillRect(0,0,c.width,c.height);

  for (let n of nodes){
    n.x += Math.sin(t*0.001 + n.y*0.01)*n.v;
    n.y += Math.cos(t*0.001 + n.x*0.01)*n.v;

    if (n.x<0) n.x=c.width;
    if (n.x>c.width) n.x=0;
    if (n.y<0) n.y=c.height;
    if (n.y>c.height) n.y=0;

    ctx.beginPath();
    ctx.arc(n.x,n.y,2 + n.v*3,0,Math.PI*2);
    ctx.fillStyle = "#7fffd4";
    ctx.fill();
  }

  requestAnimationFrame(pulse);
}

requestAnimationFrame(pulse);
</script>
</body>
</html>
HTML

# 5. Patch dashboard_server to serve static UI (safe overwrite block)
cat > mycelium/runtime/dashboard_server_patch.py << 'PY'
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/", StaticFiles(directory="mycelium/runtime/static", html=True), name="static")

@app.get("/health")
def health():
    return {"status": "mycelium-live-graph"}
PY

echo "[Mycelium Visual Layer] bootstrap complete"
echo "Run: ./venv/bin/uvicorn mycelium.runtime.dashboard_server:app --reload --port $PORT"
