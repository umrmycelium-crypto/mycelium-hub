from mycelium.runtime.ollama import ask_llm
import re


def extract_patch(text: str) -> str:
    """
    Extracts diff block from LLM output.
    """
    match = re.search(r"```diff(.*?)```", text, re.DOTALL)
    if not match:
        return ""
    return match.group(1).strip()


def generate_patch(prompt: str) -> dict:
    response = ask_llm(prompt)
    patch = extract_patch(response)

    return {
        "status": "OK" if patch else "ERROR",
        "patch": patch,
        "raw": response
    }
