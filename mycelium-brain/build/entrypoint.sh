#!/bin/bash
# Entrypoint for Mycelium Brain Docker container

set -e

echo "=========================================="
echo "Mycelium Brain Container Starting"
echo "=========================================="
echo "Date: $(date)"
echo ""

# Start Ollama in the background
echo "[1/3] Starting Ollama server..."
ollama serve &
OLLAMA_PID=$!

# Wait for Ollama to be ready
echo "[2/3] Waiting for Ollama to initialize..."
for i in {1..30}; do
    if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        echo "✓ Ollama is ready after $i seconds"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "ERROR: Ollama failed to start within 30 seconds"
        exit 1
    fi
    sleep 1
done

# Check if mycelium-brain:latest exists locally
if ollama list | grep -q "mycelium-brain:latest"; then
    echo "✓ mycelium-brain:latest is already available"
else
    echo "[3/3] Pulling mycelium-brain:latest..."
    # Try to pull from local registry first
    if ollama pull localhost:5000/mycelium/mycelium-brain:latest 2>/dev/null; then
        echo "✓ Pulled from local registry"
    else
        echo "Pulling from default registry..."
        # For now, we need to build it if not available
        # In production, this should be pre-built and pushed to a registry
        if [ -f /app/Modelfile ]; then
            echo "Building mycelium-brain:latest from Modelfile..."
            ollama create mycelium-brain:latest -f /app/Modelfile
            echo "✓ Model built successfully"
        else
            echo "ERROR: Modelfile not found and model not in registry"
            exit 1
        fi
    fi
fi

echo ""
echo "=========================================="
echo "Mycelium Brain is Ready!"
echo "=========================================="
echo "Model: mycelium-brain:latest"
echo "Ollama API: http://localhost:11434"
echo ""
echo "Available models:"
ollama list
echo ""

# Keep container running
wait $OLLAMA_PID
