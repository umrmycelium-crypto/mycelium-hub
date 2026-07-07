#!/bin/bash
# Mycelium Sovereign Keep-Alive Daemon
# Ensures the OS Server is always online 24/7

APP_PATH="/home/mycelium/mycelium-hub/app.py"
VENV_PYTHON="/home/mycelium/mycelium-hub/venv312/bin/python"
LOG_FILE="/home/mycelium/mycelium-hub/server_uptime.log"

echo "Sovereign Keep-Alive started at $(date)" >> $LOG_FILE

while true; do
    if ! pgrep -f "python app.py" > /dev/null; then
        echo "Server down. Restarting Mycelium OS... $(date)" >> $LOG_FILE
        nohup $VENV_PYTHON $APP_PATH > /dev/null 2>&1 &
    fi
    sleep 10
done
