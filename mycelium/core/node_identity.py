import uuid
import hashlib
import time

NODES = {}


def create_node_identity(name: str, secret: str):
    node_id = str(uuid.uuid4())

    token = hashlib.sha256((name + secret + str(time.time())).encode()).hexdigest()

    NODES[node_id] = {
        "name": name,
        "token": token,
        "created": time.time(),
        "trust": 1.0
    }

    return {"node_id": node_id, "token": token}


def verify_node(node_id: str, token: str):
    node = NODES.get(node_id)
    if not node:
        return False

    return node["token"] == token


def system_nodes(payload, context):
    return {
        "nodes": list(NODES.keys()),
        "count": len(NODES)
    }
