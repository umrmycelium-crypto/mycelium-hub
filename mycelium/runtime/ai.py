from mycelium.runtime.ollama import ask_llm
from mycelium.runtime.ai_parser import extract_json
from mycelium.runtime.patch_executor import apply_patch
from mycelium.runtime.memory import build_memory
import re


def clean(text: str) -> str:
    return re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', text).strip()


def ai_ask(payload, context):
    prompt = payload.get("prompt", "")

    memory = build_memory()

    enriched_prompt = f"""
You are Mycelium, an event-driven local runtime.

SYSTEM MEMORY:
{memory}

USER REQUEST:
{prompt}
"""

    raw = ask_llm(enriched_prompt)
    raw = clean(raw)

    parsed = extract_json(raw)

    if isinstance(parsed, dict) and parsed.get("action") == "patch":
        result = apply_patch(parsed)

        return {
            "status": "PATCH_APPLIED",
            "result": result
        }

    return {
        "status": "OK",
        "prompt": prompt,
        "response": raw
    }
