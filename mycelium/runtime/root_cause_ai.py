from mycelium.runtime.ollama import ask_llm
from mycelium.core.event_store import read_events


def analyze_failure():
    events = read_events()[-30:]

    prompt = f"""
You are a system debugging engine.

Analyze these events and explain root causes:

{events}

Return:
- root cause
- likely fix
- risk level
"""

    return ask_llm(prompt)
