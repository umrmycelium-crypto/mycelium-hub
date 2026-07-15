#!/bin/bash
# Mycelium Executive Agent - Always-On Daemon
# This script ensures the brain and its streams are active in the background.

set -e

# Paths
PROJECT_DIR="/home/mycelium/mycelium-hub"
PYTHON_BIN="/home/mycelium/mycelium-hub/venv312/bin/python3"

echo "Starting Mycelium Executive Daemon..."

# 1. Ensure the Brain (Ollama) is running
if ! ollama list &> /dev/null; then
    echo "Ollama not running. Starting..."
    ollama serve &
    sleep 5
fi

# 2. Activate Default Multimodal Streams
# We use the executive agent to activate the default feeds on boot
echo "Activating default multimodal streams..."
$PYTHON_BIN -c "from mycelium.agents.executive_agent import executive_agent_personal; executive_agent_personal._tool_activate_vision('iphone'); executive_agent_personal._tool_activate_audio('iphone')"

# 3. Run the MSHELL in a non-interactive headless mode if needed, 
# or just start the event-driven core.
# Since mshell.py is the UI, we actually want the CORE to be running.
# We start the bootstrap process for all workers.

echo "Bootstrapping Mycelium Core Workers..."
$PYTHON_BIN -c "from mycelium.core.workers.shell_workers import bootstrap_shell_workers; from mycelium.core.workers.sensor_workers import bootstrap_sensor_workers; from mycelium.core.workers.sentinel_worker import bootstrap_sentinel_workers; bootstrap_shell_workers(); bootstrap_sensor_workers(); bootstrap_sentinel_workers()"

echo "Starting Voice Sensing Loop..."
$PYTHON_BIN voice.py &

echo "Mycelium Executive Agent is now alive and listening."
# Keep the script running as a daemon
while true; do
    sleep 60
done
