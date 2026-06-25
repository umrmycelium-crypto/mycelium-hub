from mycelium.runtime.ollama import ask_llm


def ai_generate(prompt: str, context: dict):
    return ask_llm(prompt)
