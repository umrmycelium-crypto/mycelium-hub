import requests
import json

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"


def call_llm(prompt: str, model: str = "llama3.1") -> str:
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }

    r = requests.post(OLLAMA_URL, json=payload, timeout=120)

    if r.status_code != 200:
        raise RuntimeError(f"LLM error: {r.text}")

    return r.json()["response"]
