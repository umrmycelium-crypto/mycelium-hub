from mycelium.runtime.ai import ai_ask
from mycelium.core.intent_synthesizer import synthesize_candidates


def generate_registry_patch():
    candidates = synthesize_candidates()

    prompt = f"""
You are a system architect.

Generate a Python registry patch for Mycelium.

Rules:
- Only add safe intent handlers
- Format must be valid unified diff
- No destructive changes
- Each intent maps to a handler stub returning {"status": "OK"}

Candidates:
{candidates}
"""

    return ai_ask({
        "prompt": prompt
    }, {
        "source": "intent_patch_generator"
    })
