#!/bin/bash

PORT=${1:-8081}

echo "[Mycelium Baseline Dashboard] port $PORT"

exec ./venv/bin/uvicorn mycelium.runtime.dashboard_server:app \
  --host 127.0.0.1 \
  --port $PORT \
  --reload
