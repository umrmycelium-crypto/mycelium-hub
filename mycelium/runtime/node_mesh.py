import requests
from itertools import cycle

NODES = []
RR = None


def register_node(url: str):
    global RR
    NODES.append(url)
    RR = cycle(NODES)


def route_to_node(intent: dict):
    if not NODES:
        raise Exception("No nodes registered")

    node = next(RR)

    return requests.post(
        f"{node}/execute",
        json=intent,
        timeout=5
    ).json()


def system_mesh(payload, context):
    return {
        "nodes": NODES,
        "count": len(NODES)
    }
