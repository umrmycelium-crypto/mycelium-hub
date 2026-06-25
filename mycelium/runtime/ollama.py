import subprocess
import json


def ask_llm(prompt: str):
    """
    Streaming Ollama wrapper (qwen / llama / mistral compatible)
    """

    proc = subprocess.Popen(
        ["ollama", "run", "qwen2.5-coder:latest"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    out, _ = proc.communicate(prompt)

    return out.strip()
