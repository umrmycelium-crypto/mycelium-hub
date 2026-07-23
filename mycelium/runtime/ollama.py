import os
import subprocess
import json
import logging
from typing import Optional
import requests
from mycelium.core.models import get_llm_model, OLLAMA_URL

logger = logging.getLogger("mycelium.ollama")

# Default model can be overridden with environment variable MYCELIUM_OLLAMA_MODEL
DEFAULT_MODEL = os.environ.get("MYCELIUM_OLLAMA_MODEL")


def ask_llm(prompt: str, model: Optional[str] = None, timeout: Optional[int] = None) -> str:
    """
    Run an Ollama model and return its raw output.
    - model: optional model name; falls back to MYCELIUM_OLLAMA_MODEL env var or configured default
    - timeout: seconds to wait for a response (None = wait indefinitely)
    """
    if model is None:
        model = DEFAULT_MODEL or get_llm_model()
    
    cmd = ["ollama", "run", model]

    try:
        proc = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if timeout:
            out, err = proc.communicate(prompt, timeout=timeout)
        else:
            out, err = proc.communicate(prompt)

        if proc.returncode != 0:
            logger.error("Ollama returned non-zero (%s): %s", proc.returncode, err.strip())
            return (err or "").strip()

        return out.strip()

    except subprocess.TimeoutExpired:
        try:
            proc.kill()
        except Exception:
            pass
        logger.error("Ollama call timed out for model %s", model)
        return ""
    except Exception as e:
        logger.exception("Ollama invocation failed: %s", e)
        return ""


def ask_llm_api(prompt: str, model: Optional[str] = None) -> str:
    """
    API-based Ollama wrapper for HTTP-based interactions.
    
    Args:
        prompt: The prompt to send to the LLM
        model: Model to use (defaults to configured default)
    """
    if model is None:
        model = DEFAULT_MODEL or get_llm_model()
    
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            },
            timeout=30
        )
        if response.status_code == 200:
            return response.json().get("response", "").strip()
        else:
            logger.error("Ollama API returned HTTP %s: %s", response.status_code, response.text)
            return ""
    except Exception as e:
        logger.exception("Ollama API invocation failed: %s", e)
        return ""

