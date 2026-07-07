import json
from mycelium.core.cortex_runtime.llm import call_llm
from mycelium.core.cortex_runtime.runtime import parse_cortex_output
from mycelium.core.cortex_runtime.compiler import build_prompt


def compile_intent(user_input, registry_keys):
    prompt = build_prompt(user_input, registry_keys)

    raw = call_llm(prompt)

    parsed = parse_cortex_output(raw)

    if not parsed["ok"]:
        return {
            "status": "COMPILATION_FAILED",
            "error": parsed["error"],
            "raw": raw
        }

    return parsed["data"]
