from mycelium.runtime.ai import ai_ask


def generate_patch(prompt: str):
    """
    AI patch generator (unsafe by default — must be gated later)
    """

    return ai_ask({
        "prompt": prompt
    }, {
        "source": "repair_worker"
    })
