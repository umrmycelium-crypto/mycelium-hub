import asyncio
from mycelium.runtime.ws_graph import build_graph

# You already said you use Ollama internally
from mycelium.runtime.ollama import ask_llm


def summarize_graph(graph: dict) -> str:
    prompt = f"""
You are the internal observer of a live system called Mycelium.

Interpret the current system state as if you are describing its behavior.

Graph:
{graph}

Describe:
- what is active
- what is stable
- what is increasing in load
- any emergent behavior patterns

Keep it short, technical, and observational.
"""

    try:
        return ask_llm(prompt)
    except Exception as e:
        return f"[observer offline: {str(e)}]"


async def observer_loop(broadcast_fn):
    while True:
        graph = build_graph()
        summary = summarize_graph(graph)

        await broadcast_fn({
            "type": "system.observer",
            "summary": summary
        })

        await asyncio.sleep(2.0)
