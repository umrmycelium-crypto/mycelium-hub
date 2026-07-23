import uuid
import hashlib
import time
import os
import json
from typing import Dict, Any, Optional

NODES: Dict[str, Dict[str, Any]] = {}
IDENTITY_FILE = "state/node_identity.json"


def get_or_create_local_identity(name: str = "local-node", secret: str = "mycelium-mesh-secret") -> Dict[str, str]:
    """
    Retrieves the local node's identity from disk, or creates a new persistent identity.
    """
    if os.path.exists(IDENTITY_FILE):
        try:
            with open(IDENTITY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                NODES[data["node_id"]] = data
                return data
        except Exception:
            pass

    os.makedirs(os.path.dirname(IDENTITY_FILE), exist_ok=True)
    identity = create_node_identity(name, secret)
    try:
        with open(IDENTITY_FILE, "w", encoding="utf-8") as f:
            json.dump(NODES[identity["node_id"]], f, indent=4)
    except Exception:
        pass
    return identity


def create_node_identity(name: str, secret: str) -> Dict[str, str]:
    """Generates a node ID and secret token for mesh authentication."""
    node_id = str(uuid.uuid4())
    token = hashlib.sha256(f"{name}:{secret}:{time.time()}".encode("utf-8")).hexdigest()

    NODES[node_id] = {
        "node_id": node_id,
        "name": name,
        "token": token,
        "created": time.time(),
        "trust": 1.0
    }

    return {"node_id": node_id, "token": token, "name": name}


def verify_node(node_id: str, token: str) -> bool:
    """Verifies if a node ID matches its authentication token."""
    node = NODES.get(node_id)
    if not node:
        return False
    return node.get("token") == token


def register_remote_node(node_id: str, name: str, token: str, trust: float = 1.0):
    """Registers a remote node's verified credentials."""
    NODES[node_id] = {
        "node_id": node_id,
        "name": name,
        "token": token,
        "created": time.time(),
        "trust": trust
    }


def system_nodes(payload: Optional[Dict[str, Any]] = None, context: Optional[Any] = None) -> Dict[str, Any]:
    """Returns all registered mesh nodes."""
    return {
        "nodes": list(NODES.keys()),
        "count": len(NODES),
        "details": [
            {"node_id": nid, "name": info["name"], "trust": info.get("trust", 1.0)}
            for nid, info in NODES.items()
        ]
    }

