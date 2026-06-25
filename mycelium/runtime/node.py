import os
import time
import json
from mycelium.core.event_store import read_events, append_event
from mycelium.core.router import route

NODE_ID = os.getenv("MYCELIUM_NODE_ID", "node-1")


def run_node_loop():
    print(f"[{NODE_ID}] starting runtime loop")

    last_index = 0

    while True:
        events = read_events()

        new_events = events[last_index:]

        for event in new_events:
            try:
                intent = event.get("payload", {})
                intent["name"] = event.get("event")

                route(intent)

            except Exception as e:
                append_event({
                    "event": "node.error",
                    "node": NODE_ID,
                    "error": str(e),
                    "timestamp": time.time()
                })

        last_index = len(events)
        time.sleep(0.5)


if __name__ == "__main__":
    run_node_loop()
