#!/bin/bash

echo "=== MYCELIUM HANDOFF PACKET ==="
echo "System: mycelium-hub"
echo "Mode: self-perception reactive graph"
echo "Runtime: FastAPI + WebSocket"
echo "Dashboard: / running uvicorn static canvas UI"
echo ""
echo "State:"
cat mycelium/state/snapshot.json
echo ""
echo "Next intended layer:"
echo "- semantic graph cognition layer"
echo "- anomaly detection overlay"
echo "- memory decay system"
echo "================================"
