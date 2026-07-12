#!/bin/bash
# Mycelium Brain Fine-Tuning Build Script
# This script builds the branched custom models for Mycelium OS: public and personal.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "=========================================="
echo "Mycelium Brain Branching Build"
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

# Check for training data
TRAINING_FILE="$SCRIPT_DIR/training_data/mycelium_training.jsonl"
if [ -f "$TRAINING_FILE" ]; then
    echo "✓ Training data found: $TRAINING_FILE"
else
    echo "WARNING: No training data found at $TRAINING_FILE"
    echo "Building personal brain without fine-tuning data (system prompt only)"
fi

echo ""
echo "[3/5] Building branched models..."

# Build the models
cd "$SCRIPT_DIR"

# Ollama create command based on version
OLLAMA_VERSION=$(ollama --version | awk '{print $NF}')
echo "Ollama version: $OLLAMA_VERSION"

# Define models to build
MODELS_TO_BUILD=(
    "mycelium-brain-public:latest"
    "mycelium-brain-personal:latest"
)

# Define corresponding Modelfiles
MODELFILES=(
    "Modelfile.public"
    "Modelfile.personal"
)

# Loop through and build each model
for i in "${!MODELS_TO_BUILD[@]}"; do
    MODEL_NAME="${MODELS_TO_BUILD[$i]}"
    MODELFILE="${MODELFILES[$i]}"
    
    echo "Building $MODEL_NAME using $MODELFILE..."
    
    if [[ "$OLLAMA_VERSION" == 0.30.* ]]; then
        ollama create "$MODEL_NAME" -f "$MODELFILE"
    else
        ollama build "$MODEL_NAME" -f "$MODELFILE"
    fi
done

echo ""
echo "[4/5] Verifying builds..."

# Verify each model
for MODEL_NAME in "${MODELS_TO_BUILD[@]}"; do
    if ollama list | grep -q "$MODEL_NAME"; then
        echo "✓ $MODEL_NAME successfully built!"
    else
        echo "ERROR: Model build for $MODEL_NAME may have failed."
        exit 1
    fi
done

echo ""
echo "[5/5] Creating Docker image for distribution..."

# Create Dockerfile for the model
cat > "$BUILD_DIR/Dockerfile" << 'EOF'
# Mycelium Brain Docker Image
# Distributes the custom branched models

FROM ollama/ollama:latest

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
EOF

chmod +x "$BUILD_DIR/entrypoint.sh"

echo "✓ Dockerfile created in $BUILD_DIR/Dockerfile"
echo ""

echo "=========================================="
echo "Build Summary"
echo "=========================================="
echo "✓ Modelfiles: Modelfile.public, Modelfile.personal"
echo "✓ Models: mycelium-brain-public:latest, mycelium-brain-personal:latest"
echo "✓ Build directory: $BUILD_DIR"
echo "✓ Dockerfile: $BUILD_DIR/Dockerfile"
echo ""
echo "To use the models:"
echo "  ollama run mycelium-brain-public:latest"
echo "  ollama run mycelium-brain-personal:latest"
echo ""
echo "To build Docker image:"
echo "  cd $BUILD_DIR && docker build -t mycelium-brain:latest ."
echo ""
echo "To push to registry:"
echo "  docker tag mycelium-brain:latest localhost:5000/mycelium/mycelium-brain:latest"
echo "  docker push mycelium-brain:latest localhost:5000/mycelium/mycelium-brain:latest"
echo ""
echo "Build complete!"
