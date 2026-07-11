# Mistral API Setup for Mycelium OS

This guide explains how to connect your local brain to Mistral's API.

## ⚠️ SECURITY WARNING

**NEVER commit API keys to version control!** 
Always use environment variables.

## Quick Start

```bash
# 1. Get a new API key from https://console.mistral.ai/
# 2. Set it as environment variable

# Linux/Mac (add to ~/.bashrc or ~/.zshrc)
echo 'export MISTRAL_API_KEY="your-new-api-key"' >> ~/.bashrc
source ~/.bashrc

# Or temporary for this session only
export MISTRAL_API_KEY="your-new-api-key"

# 3. Test it
python test_mistral.py
```

---

## Problem

The error you're seeing:
```
API error from llamacpp (model: devstral): LLM backend error [llamacpp]
status: 400 Bad Request
payload_summary: {"model":"devstral","message_count":2,"approx_chars":28858,...}
```

This occurs because:
1. The local `devstral` model served via llamacpp has a limited context window
2. Your request has ~28,858 characters, exceeding the model's limit
3. The 400 Bad Request is the model rejecting the oversized input

## Solutions

You have three options:

### Option 1: Use Mistral Cloud API (Recommended)

1. **Get a Mistral API key**
   - Sign up at https://console.mistral.ai/
   - Navigate to API Keys section
   - Create a new API key

2. **Configure the API key SECURELY**
   
   **✅ DO THIS (Environment Variable - Recommended):**
   ```bash
   # Add to your ~/.bashrc or ~/.zshrc
   echo 'export MISTRAL_API_KEY="your-api-key-here"' >> ~/.bashrc
   source ~/.bashrc
   ```
   
   **OR (Temporary for testing):**
   ```bash
   export MISTRAL_API_KEY="your-api-key-here"
   ```
   
   **OR (.env file):**
   ```bash
   echo "MISTRAL_API_KEY=your-api-key-here" > .env
   # Then load it before running Python
   source .env
   ```
   
   **❌ NEVER DO THIS:**
   ```python
   # HARDCODED KEYS IN CODE - DANGEROUS!
   MISTRAL_API_KEY = "your-api-key-here"  # NEVER COMMIT THIS!
   ```

3. **Use Mistral models**
   You can now use any Mistral model:
   - `mistral-tiny` (32K context)
   - `mistral-small` (32K context)
   - `mistral-medium` (32K context)
   - `mistral-large` (128K context)

   Example:
   ```python
   from mycelium.core.llm_runtime import LLMRuntime
   
   # Use Mistral's cloud API
   response = LLMRuntime.call("Your prompt here", model="mistral-small")
   ```

4. **Set as default**
   To use Mistral by default:
   ```python
   from mycelium.core.models import set_default_model
   set_default_model("mistral-small")
   ```

### Option 2: Increase Llamacpp Context Window

If you want to continue using local llamacpp with devstral:

1. **Start llamacpp with larger context**
   ```bash
   # Example: Start devstral with 32K context window
   llama-server --model devstral.gguf --ctx-size 32768 --port 8080
   ```

2. **Update model configuration**
   Edit `mycelium/core/models.py`:
   ```python
   # Add devstral to Ollama models (it will be routed to llamacpp)
   LLM_MODELS = {
       ...
       "devstral": "devstral",
   }
   ```

### Option 3: Use Context Truncation (Already Implemented)

The system now automatically truncates long prompts to fit within model limits.
The truncation keeps:
- Full system prompt
- Recent cognitive context
- Full user input

This happens transparently in `mycelium/llm/ollama_intent.py`.

## Unified LLM Runtime

The new `mycelium/core/llm_runtime.py` provides a unified interface:

```python
from mycelium.core.llm_runtime import LLMRuntime

# Automatic routing based on model name
response = LLMRuntime.call("Your prompt", model="devstral")  # Uses llamacpp
response = LLMRuntime.call("Your prompt", model="mistral-small")  # Uses Mistral API
response = LLMRuntime.call("Your prompt", model="llama3.1")  # Uses Ollama

# With chat context
response = LLMRuntime.call_with_context(
    system_prompt="You are a helpful assistant",
    user_prompt="Hello, how are you?",
    model="mistral-small"
)
```

## Configuration Reference

### `mycelium/core/models.py`

```python
# Ollama URL (default)
OLLAMA_URL = "http://localhost:11434/api/generate"

# Llamacpp URL (for local devstral)
LLAMACPP_URL = "http://127.0.0.1:8080/v1/chat/completions"

# Mistral API
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"
MISTRAL_API_KEY = None  # Set this to your API key

# Models
LLM_MODELS = {
    "default": "llama3.1",
    "llama3.1": "llama3.1",
    "devstral": "devstral",  # Will use llamacpp
    "mistral-small": "mistral-small",  # Will use Mistral API
}
```

## Migration Guide

If you're currently using the local brain (mycelium-brain:latest):

1. **Pull the model with Ollama**
   ```bash
   ollama pull mycelium-brain:latest
   ```

2. **Or use via Mistral API**
   ```python
   from mycelium.core.models import set_default_model
   set_default_model("mistral-small")
   ```

## Troubleshooting

### "Cannot connect to llamacpp"
- Make sure llamacpp server is running: `llama-server --port 8080`
- Verify the model is loaded

### "Mistral API key not configured"
- Set `MISTRAL_API_KEY` in `mycelium/core/models.py`

### "400 Bad Request" with long prompts
- Use a model with larger context (mistral-large has 128K)
- Or enable context truncation (already implemented)

## Model Comparison

| Model | Backend | Context | Location |
|-------|---------|---------|----------|
| llama3.1 | Ollama | 128K | Local |
| mycelium-brain | Ollama | Varies | Local |
| devstral | Llamacpp | Configurable | Local |
| mistral-tiny | Mistral API | 32K | Cloud |
| mistral-small | Mistral API | 32K | Cloud |
| mistral-medium | Mistral API | 32K | Cloud |
| mistral-large | Mistral API | 128K | Cloud |
