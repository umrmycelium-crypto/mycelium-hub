# Model Configuration

This document explains how models are configured and used in Mycelium OS.

## Overview

Mycelium OS now uses a centralized model configuration system located in `mycelium/core/models.py`. This allows you to:

- View all available LLM models
- Add new models to the system
- Remove models from the system  
- Change the default model
- Use any configured model throughout the codebase

## Available Models

By default, the following LLM models are configured:

- `llama3.1` (default)
- `llama3.1:latest`
- `qwen2.5-coder:latest`
- `mycelium-brain:latest`

## Usage

### Getting the current model

```python
from mycelium.core.models import get_llm_model

# Get default model
model = get_llm_model()  # Returns "llama3.1"

# Get specific model
model = get_llm_model("mycelium-brain:latest")  # Returns "mycelium-brain:latest"
# Falls back to default if model doesn't exist
model = get_llm_model("nonexistent")  # Returns "llama3.1"
```

### Listing available models

```python
from mycelium.core.models import list_available_models

models = list_available_models()
# Returns: ['llama3.1', 'llama3.1', 'llama3.1:latest', 'qwen2.5-coder:latest', 'mycelium-brain:latest']
```

### Adding a new model

```python
from mycelium.core.models import add_model

# Add a model with the same name and identifier
add_model("new-model:latest")

# Add a model with custom name and identifier
add_model("my-custom-name", "actual-model:tag")
```

### Removing a model

```python
from mycelium.core.models import remove_model

remove_model("model-to-remove")
```

### Setting the default model

```python
from mycelium.core.models import set_default_model

set_default_model("mycelium-brain:latest")
```

## Integration

The following components have been updated to use the centralized model configuration:

- `mycelium/runtime/ollama.py` - Ollama wrapper functions
- `mycelium/core/cortex_runtime/llm.py` - LLM calling functions
- `mycelium/llm/ollama_intent.py` - Intent parsing with Ollama
- `mycelium/core/agent_base.py` - Base agent class
- `mycelium/agents/creative_cores.py` - Creative core agents
- `mycelium/agents/router_agent.py` - Intent routing agent
- `mycelium/agents/decomposer.py` - Task decomposition agent
- `app.py` - Main application
- `voice.py` - Voice model configuration

## Voice Models

Voice/TTS models are also configured in the same file:

- `VOICE_MODEL_PATH`: Path to the voice model file (`models/en_US-lessac-medium.onnx`)
- `VOICE_MODEL_CONFIG`: Path to the voice model configuration file
- `WHISPER_MODEL_TYPE`: Type of Whisper model to use (`base`)

## Model Configuration Details

The `LLM_MODELS` dictionary maps model names to their identifiers:

```python
LLM_MODELS = {
    "default": "llama3.1",
    "llama3.1": "llama3.1",
    "llama3.1:latest": "llama3.1:latest",
    "qwen2.5-coder:latest": "qwen2.5-coder:latest",
    "mycelium-brain:latest": "mycelium-brain:latest",
}
```

You can add your own models by either:
1. Directly editing this dictionary
2. Using the `add_model()` function at runtime

## Ollama Integration

To use these models, you need Ollama running locally with the models pulled:

```bash
# Pull the default models
ollama pull llama3.1
ollama pull qwen2.5-coder

# Pull your custom model
ollama pull mycelium-brain:latest
```

The system will automatically use the configured models when making requests to the Ollama API.