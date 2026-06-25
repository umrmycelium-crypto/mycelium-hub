#!/bin/bash
set -e

SNAPSHOT="mycelium/state/snapshot.json"

if [ ! -f "$SNAPSHOT" ]; then
  echo "[Mycelium] no snapshot found"
  exit 1
fi

PORT=$(python3 -c "import json; print(json.load(open('$SNAPSHOT'))['active_ports']['dashboard'])")

echo "[Mycelium] restoring system on port $PORT"

pkill -f uvicorn || true
sleep 1

./run_dashboard.sh $PORT
