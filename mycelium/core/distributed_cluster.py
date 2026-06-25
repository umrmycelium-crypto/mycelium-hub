import uuid
from time import time

NODES = {}


def register_node(name: str, metadata: dict = None):
    node_id = str(uuid.uuid4())

    NODES[node_id] = {
        "name": name,
        "metadata": metadata or {},
        "created_at": time(),
        "status": "active"
    }

    return {"node_id": node_id}


def list_nodes():
    return NODES


def broadcast(event: dict):
    """
    Logical broadcast (no networking yet, simulation layer).
    """

    results = []

    for node_id, node in NODES.items():
        results.append({
            "node": node["name"],
            "status": "received",
            "event": event
        })

    return {
        "delivered_to": len(NODES),
        "results": results
    }


def system_cluster(payload, context):
    return {
        "nodes": len(NODES),
        "active": list(NODES.keys())
    }
