#!/bin/bash
# Mycelium Brain Fine-Tuning Build Script
# This script builds the custom mycelium-brain:latest model for Mycelium OS

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "=========================================="
echo "Mycelium Brain Fine-Tuning Build"
echo "=========================================="
echo "Script Directory: $SCRIPT_DIR"
echo "Project Directory: $PROJECT_DIR"
echo ""

# Check prerequisites
echo "[1/5] Checking prerequisites..."

# Check Ollama
if ! command -v ollama &> /dev/null; then
    echo "ERROR: Ollama is not installed. Please install Ollama first."
    exit 1
fi

echo "✓ Ollama is installed (version: $(ollama --version))"

# Check if Ollama is running
if ! ollama list &> /dev/null; then
    echo "ERROR: Ollama service is not running. Please start Ollama."
    exit 1
fi

echo "✓ Ollama service is running"

# Check for base model
BASE_MODEL="llama3.1:latest"
if ! ollama list | grep -q "$BASE_MODEL"; then
    echo "Pulling base model: $BASE_MODEL"
    ollama pull "$BASE_MODEL"
else
    echo "✓ Base model $BASE_MODEL is available"
fi

echo ""
echo "[2/5] Creating build directory..."
BUILD_DIR="$SCRIPT_DIR/build"
mkdir -p "$BUILD_DIR"

# Copy Modelfile
echo "✓ Using Modelfile from $SCRIPT_DIR/Modelfile"

# Check for training data
TRAINING_FILE="$SCRIPT_DIR/training_data/mycelium_training.jsonl"
if [ -f "$TRAINING_FILE" ]; then
    echo "✓ Training data found: $TRAINING_FILE"
else
    echo "WARNING: No training data found at $TRAINING_FILE"
    echo "Building without fine-tuning data (system prompt only)"
fi

echo ""
echo "[3/5] Building mycelium-brain:latest..."

# Build the model
cd "$SCRIPT_DIR"

# First, try to create the model with the Modelfile
echo "Building with Ollama..."
echo "Command: ollama create mycelium-brain:latest -f Modelfile"

# Note: As of Ollama 0.30.4, the 'ollama create' command with Modelfile is the correct approach
# However, for fine-tuning we need to use the appropriate command based on Ollama version

# Check Ollama version for create command
OLLAMA_VERSION=$(ollama --version | cut -d' ' -f3)
echo "Ollama version: $OLLAMA_VERSION"

# For Ollama 0.30.x, use 'ollama create'
if [[ "$OLLAMA_VERSION" == 0.30.* ]]; then
    echo "Using ollama create for version $OLLAMA_VERSION"
    ollama create mycelium-brain:latest -f Modelfile
else
    echo "Using ollama build for version $OLLAMA_VERSION"
    ollama build mycelium-brain:latest -f Modelfile
fi

echo ""
echo "[4/5] Verifying build..."

# Check if model was created
if ollama list | grep -q "mycelium-brain:latest"; then
    echo "✓ mycelium-brain:latest successfully built!"
    echo ""
    echo "Model details:"
    ollama show mycelium-brain:latest
else
    echo "ERROR: Model build may have failed. Checking logs..."
    exit 1
fi

echo ""
echo "[5/5] Creating Docker image for distribution..."

# Create Dockerfile for the model
cat > "$BUILD_DIR/Dockerfile" << 'EOF'
# Mycelium Brain Docker Image
# Distributes the custom fine-tuned model

FROM ollama/ollama:latest

# Copy the model file (will be built separately)
# The model will be pulled at runtime or mounted as a volume

# Set up entrypoint
WORKDIR /app
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["serve"]
EOF

# Create entrypoint script
cat > "$BUILD_DIR/entrypoint.sh" << 'EOF'
#!/bin/bash
# Entrypoint for mycelium-brain container

set -e

echo "Starting Mycelium Brain container..."

# Pull the model if not already present
if ! ollama list | grep -q "mycelium-brain:latest"; then
    echo "Pulling mycelium-brain:latest..."
    ollama pull mycelium-brain:latest
else
    echo "mycelium-brain:latest is already available"
fi

# Start Ollama in the background
ollama serve &

# Keep container running
wait
EOF

chmod +x "$BUILD_DIR/entrypoint.sh"

echo "✓ Dockerfile created in $BUILD_DIR/Dockerfile"
echo ""

echo "=========================================="
echo "Build Summary"
echo "=========================================="
echo "✓ Modelfile: $SCRIPT_DIR/Modelfile"
echo "✓ Model: mycelium-brain:latest"
echo "✓ Build directory: $BUILD_DIR"
echo "✓ Dockerfile: $BUILD_DIR/Dockerfile"
echo ""
echo "To use the model:"
echo "  ollama run mycelium-brain:latest"
echo ""
echo "To build Docker image:"
echo "  cd $BUILD_DIR && docker build -t mycelium-brain:latest ."
echo ""
echo "To push to registry:"
echo "  docker tag mycelium-brain:latest localhost:5000/mycelium/mycelium-brain:latest"
echo "  docker push localhost:5000/mycelium/mycelium-brain:latest"
echo ""
echo "Build complete!"
