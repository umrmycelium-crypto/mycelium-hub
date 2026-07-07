#!/bin/bash

# Mycelium Fix & Restart Script
# This script applies all fixes and restarts the system

echo "🔧 Mycelium Fix & Restart Script"
echo "================================"
echo ""

# Stop existing processes
echo "🛑 Stopping existing processes..."
pkill -f "uvicorn.*daemon.server" 2>/dev/null || true
pkill -f "http.server 8082" 2>/dev/null || true
pkill -f "keep_alive" 2>/dev/null || true
sleep 2

# Kill any remaining python processes on these ports
fuser -k 8000/tcp 2>/dev/null
fuser -k 8082/tcp 2>/dev/null
sleep 1

# Apply state fix
echo "🔧 Fixing state file..."
cd /home/mycelium/mycelium-hub
python3 fix_state.py
sleep 1

# Restart with fresh state
echo "🚀 Restarting Mycelium system..."
cd /home/mycelium/mycelium-hub

# Start daemon
python3 -c "import uvicorn; uvicorn.run('mycelium-hub.daemon.server:app', host='0.0.0.0', port=8000)" &
API_PID=$!
echo "✅ Daemon started (PID: $API_PID)"

# Wait for daemon to start
sleep 3

# Start HTTP server for dashboard
python3 -m http.server 8082 &
UI_PID=$!
echo "✅ Dashboard server started (PID: $UI_PID)"

# Wait for servers to start
sleep 3

# Health check
echo ""
echo "🏥 Health Check:"
if curl -s "http://127.0.0.1:8000/status" >/dev/null 2>&1; then
    echo "✅ Daemon is running"
    TICK=$(curl -s "http://127.0.0.1:8000/status" | python3 -c "import sys,json; print(json.load(sys.stdin).get('tick',0))" 2>/dev/null)
    echo "   Tick: $TICK"
else
    echo "❌ Daemon failed to start"
fi

if curl -s "http://127.0.0.1:8082/dashboard/" >/dev/null 2>&1; then
    echo "✅ Dashboard is running"
else
    echo "❌ Dashboard failed to start"
fi

if curl -s "http://127.0.0.1:8082/campaign/" >/dev/null 2>&1; then
    echo "✅ Campaign page is accessible"
else
    echo "❌ Campaign page not accessible"
fi

echo ""
echo "🎯 Access Points:"
echo "   Dashboard: http://127.0.0.1:8082/dashboard/"
echo "   Campaign:  http://127.0.0.1:8082/campaign/"
echo "   API:       http://127.0.0.1:8000/status"
echo "   WebSocket: ws://127.0.0.1:8000/ws"
echo ""
echo "✨ Fixes Applied:"
echo "   ✓ Bounded idea strength values (0-1 range)"
echo "   ✓ Improved dashboard visibility (colors, sizes)"
echo "   ✓ Added favicon (no more 404)"
echo "   ✓ Added links between nodes for better visualization"
echo "   ✓ Fixed CSS selector errors"
echo "   ✓ Added accessibility features"
echo "   ✓ Campaign page accessible at /campaign/"
echo ""
echo "💡 Note: If nodes still appear too small or invisible:"
echo "   1. Clear your browser cache (Ctrl+Shift+R)"
echo "   2. Try a different browser (Chromium recommended)"
echo "   3. Wait 5-10 seconds for the 3D library to load"
echo ""

# Start keep-alive monitor in background
nohup /home/mycelium/mycelium-hub/keep_alive_v3.sh >> /tmp/mycelium_restart.log 2>&1 &
echo "✅ Keep-alive monitor started"

wait
