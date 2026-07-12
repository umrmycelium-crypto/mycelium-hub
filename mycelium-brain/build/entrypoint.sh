#!/bin/bash
# Entrypoint for mycelium-brain container

set -e

echo "Starting Mycelium Brain container..."

# Pull the models if not already present
for model in mycelium-brain-public:latest mycelium-brain-personal:latest; do
    if ! ollama list | grep -q "$model"; then
        echo "Pulling $model..."
        ollama pull "$model"
    fi
done

# Start Ollama in the background
ollama serve &

# Keep container running
wait
