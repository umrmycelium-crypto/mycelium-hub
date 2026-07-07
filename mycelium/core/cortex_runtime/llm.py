import requests
import json
from mycelium.core.models import get_llm_model, OLLAMA_URL as OLLAMA_URL_CONFIG


def call_llm(prompt: str, model: str = None) -> str:
    if model is None:
        model = get_llm_model()
    
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }

    r = requests.post(OLLAMA_URL_CONFIG, json=payload, timeout=120)

    if r.status_code != 200:
        raise RuntimeError(f"LLM error: {r.text}")

    return r.json()["response"]
