from mycelium.runtime.ai import ai_ask


def generate_patch(failure):
    prompt = f"""
You are a repair system.

Given this failure:
{failure}

Return a safe patch proposal:
- no code execution
- only structured explanation
"""

    return ai_ask({"prompt": prompt}, {"source": "repair"})
