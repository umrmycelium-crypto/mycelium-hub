import asyncio
import time
from collections import deque
from fastapi import WebSocket

from mycelium.core.execution_trace import get_trace
from mycelium.core.registry_core import get_registry
from mycelium.core.secure_ledger import LEDGER

clients = set()
_signal_history = deque(maxlen=120)


def _pulse(trace_len: int) -> float:
    now = time.time()
    _signal_history.append((now, trace_len))

    if len(_signal_history) < 2:
        return 1.0

    (t0, v0) = _signal_history[0]
    (t1, v1) = _signal_history[-1]

    rate = (v1 - v0) / max(t1 - t0, 0.001)

    return max(0.6, min(1.0 + rate / 25.0, 3.0))


def build_graph():
    trace = get_trace(50)
    registry = list(get_registry())

    pulse = _pulse(len(trace))

    return {
        "type": "system.graph",
        "meta": {"pulse": pulse},

        # 🧠 MULTI-LAYER COGNITION MODEL
        "nodes": [
            # perception layer
            {"id": "sensor.audio", "layer": "perception", "pulse": pulse * 1.3},
            {"id": "sensor.video", "layer": "perception", "pulse": pulse * 1.1},

            # working memory
            {"id": "event_bus", "layer": "memory", "pulse": pulse},
            {"id": "trace", "layer": "memory", "size": len(trace), "pulse": pulse},

            # long-term memory
            {"id": "registry", "layer": "memory", "size": len(registry), "pulse": pulse * 0.7},
            {"id": "ledger", "layer": "memory", "size": len(LEDGER), "pulse": pulse * 0.8},

            # reasoning layer
            {"id": "ai_runtime", "layer": "reasoning", "pulse": pulse * 1.5},
            {"id": "ai_observer", "layer": "reasoning", "pulse": pulse * 1.2},
        ],

        "links": [
            # perception → memory
            {"source": "sensor.audio", "target": "event_bus"},
            {"source": "sensor.video", "target": "event_bus"},

            # memory flow
            {"source": "event_bus", "target": "trace"},
            {"source": "event_bus", "target": "registry"},
            {"source": "registry", "target": "ledger"},

            # reasoning loop
            {"source": "ai_runtime", "target": "event_bus"},
            {"source": "ai_observer", "target": "ai_runtime"},
        ]
    }


async def graph_stream(ws: WebSocket):
    await ws.accept()
    clients.add(ws)

    try:
        while True:
            await ws.send_json(build_graph())
            await asyncio.sleep(0.35)

    finally:
        clients.discard(ws)
