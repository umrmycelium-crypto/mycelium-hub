#!/bin/bash

# Mycelium Cortex Keep-Alive Script
# Monitors and restarts daemon (8000) and HTTP server (8082)

DAEMON_LOG="/tmp/daemon_autopilot.log"
HTTP_LOG="/tmp/http_autopilot.log"

while true; do
    # Check daemon on port 8000
    if ! ss -tlnp | grep -q ':8000 '; then
        echo "$(date) - Daemon down, restarting..." >> "$DAEMON_LOG"
        cd /home/mycelium/mycelium-hub && PYTHONPATH=/home/mycelium/mycelium-hub \
            nohup python3 -c "import uvicorn; uvicorn.run('mycelium-hub.daemon.server:app', host='0.0.0.0', port=8000)" \
            >> "$DAEMON_LOG" 2>&1 &
        sleep 5
    fi

    # Check HTTP server on port 8082
    if ! ss -tlnp | grep -q ':8082 '; then
        echo "$(date) - HTTP server down, restarting..." >> "$HTTP_LOG"
        cd /home/mycelium/mycelium-hub/mycelium-hub && \
            nohup python3 -m http.server 8082 >> "$HTTP_LOG" 2>&1 &
        sleep 5
    fi

    sleep 30
done
