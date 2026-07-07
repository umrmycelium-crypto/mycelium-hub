import subprocess
import json
from mycelium.core.models import get_llm_model, OLLAMA_URL
import requests


def ask_llm(prompt: str, model: str = None):
    """
    Streaming Ollama wrapper (qwen / llama / mistral compatible)
    
    Args:
        prompt: The prompt to send to the LLM
        model: Model to use (defaults to configured default)
    """
    if model is None:
        model = get_llm_model()
    
    # For subprocess-based interaction
    proc = subprocess.Popen(
        ["ollama", "run", model],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    out, _ = proc.communicate(prompt)

    return out.strip()


def ask_llm_api(prompt: str, model: str = None):
    """
    API-based Ollama wrapper for more control.
    
    Args:
        prompt: The prompt to send to the LLM
        model: Model to use (defaults to configured default)
    """
    if model is None:
        model = get_llm_model()
    
    import requests
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": model,
            "prompt": prompt,
            "stream": False
        }
    )
    return response.json().get("response", "")
