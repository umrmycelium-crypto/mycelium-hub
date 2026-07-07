import os
import subprocess
import json
import logging
from typing import Optional

logger = logging.getLogger("mycelium.ollama")

# Default model can be overridden with environment variable MYCELIUM_OLLAMA_MODEL
DEFAULT_MODEL = os.environ.get("MYCELIUM_OLLAMA_MODEL", "qwen2.5-coder:latest")


def ask_llm(prompt: str, model: Optional[str] = None, timeout: Optional[int] = None) -> str:
    """
    Run an Ollama model and return its raw output.
    - model: optional model name (e.g. 'qwen2.5-coder:latest'); falls back to DEFAULT_MODEL
    - timeout: seconds to wait for a response (None = wait indefinitely)

    Set MYCELIUM_OLLAMA_MODEL environment variable to change default globally.
    """

    model = model or DEFAULT_MODEL
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
