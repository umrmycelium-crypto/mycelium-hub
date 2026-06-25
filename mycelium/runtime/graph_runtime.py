import asyncio
from mycelium.core.execution_trace import get_trace
from mycelium.runtime.graph_engine import GRAPH
from mycelium.runtime.ws_bridge import broadcast

class GraphRuntime:
    def __init__(self):
        self.tick = 0

    async def run(self):
        while True:
            self.tick += 1

            trace = get_trace(50)

            # ingest into graph model
            GRAPH.ingest(trace)

            payload = {
                "type": "graph.update",
                "tick": self.tick,
                "graph": GRAPH.snapshot()
            }

            await broadcast(payload)

            # stable refresh rate (important for animation)
            await asyncio.sleep(0.6)

RUNTIME = GraphRuntime()
