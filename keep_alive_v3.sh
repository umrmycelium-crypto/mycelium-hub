#!/bin/bash

# Mycelium Cortex Keep-Alive v3 - Ultimate Resilience
# Monitors daemon (8000), HTTP server (8082), with health checks and timeouts

LOG_FILE="/tmp/mycelium_autopilot_v3.log"

echo "=== Mycelium Autopilot v3 Started $(date) ===" >> "$LOG_FILE"

# Function to start daemon
start_daemon() {
    cd /home/mycelium/mycelium-hub
    PYTHONPATH=/home/mycelium/mycelium-hub \
        nohup python3 -c "import uvicorn; uvicorn.run('mycelium-hub.daemon.server:app', host='0.0.0.0', port=8000)" \
        >> "$LOG_FILE" 2>&1 &
    echo "[$(date)] Daemon restarted" >> "$LOG_FILE"
}

# Function to start HTTP server
start_http() {
    cd /home/mycelium/mycelium-hub/mycelium-hub
    nohup python3 -m http.server 8082 >> "$LOG_FILE" 2>&1 &
    echo "[$(date)] HTTP server restarted" >> "$LOG_FILE"
}

# Initial start
start_daemon
start_http
sleep 10

# Main monitoring loop
while true; do
    # Check daemon on port 8000
    if ! ss -tlnp | grep -q ':8000 '; then
        echo "[$(date)] Daemon down, restarting..." >> "$LOG_FILE"
        pkill -f "mycelium-hub.daemon.server" 2>/dev/null
        sleep 2
        start_daemon
    fi

    # Check HTTP server on port 8082
    if ! ss -tlnp | grep -q ':8082 '; then
        echo "[$(date)] HTTP server down, restarting..." >> "$LOG_FILE"
        pkill -f "http.server 8082" 2>/dev/null
        sleep 2
        start_http
    fi

    # Health check daemon with timeout
    if ! timeout 5 curl -s http://127.0.0.1:8000/status >/dev/null 2>&1; then
        echo "[$(date)] Daemon health check failed, restarting..." >> "$LOG_FILE"
        pkill -9 -f "mycelium-hub.daemon.server" 2>/dev/null
        sleep 2
        start_daemon
    fi

    # Check tick progress (watchdog fallback)
    CURRENT_TICK=$(timeout 5 curl -s http://127.0.0.1:8000/status 2>/dev/null | python3 -c "import sys,json; print(json.load(sys.stdin).get('tick',0))" 2>/dev/null)
    
    # Store last tick in a file for comparison
    LAST_TICK_FILE="/tmp/mycelium_last_tick.txt"
    if [ -f "$LAST_TICK_FILE" ]; then
        LAST_TICK=$(cat "$LAST_TICK_FILE")
        if [ "$CURRENT_TICK" = "$LAST_TICK" ]; then
            echo "[$(date)] Tick not progressing ($CURRENT_TICK), daemon may be hung" >> "$LOG_FILE"
            # The daemon's internal watchdog should handle this, but we can restart if needed
            # after a longer period
        fi
    fi
    echo "$CURRENT_TICK" > "$LAST_TICK_FILE"

    sleep 15
done
