#!/bin/bash
set -e

mkdir -p mycelium/state

echo "[Mycelium] generating system snapshot..."

cat > mycelium/state/snapshot.json << JSON
{
  "system": "mycelium-hub",
  "timestamp": "$(date -Iseconds)",
  "active_ports": {
    "dashboard": 8081
  },
  "services": {
    "uvicorn": "dashboard_server",
    "websocket": true
  },
  "graph_mode": "self_perception",
  "runtime": {
    "trace_enabled": true,
    "ws_enabled": true
  }
}
JSON

echo "[Mycelium] snapshot written to mycelium/state/snapshot.json"
