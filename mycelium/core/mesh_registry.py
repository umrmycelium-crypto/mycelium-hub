import json
import os
import threading
import logging
from typing import Any, Dict, List, Optional
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MeshRegistry")

class MeshRegistry:
    """
    The MeshRegistry tracks the topography of the Mycelium network.
    It maintains a list of active nodes and their capabilities (Hardware, OS, Agents).
    """
    def __init__(self, node_id: str, state_file: str = "state/mesh_registry.json"):
        self.node_id = node_id
        self.state_file = state_file
        self.nodes: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.Lock()
        self._load_registry()

    def update_node(self, node_id: str, manifest: Dict[str, Any]):
        """Updates or adds a node to the registry."""
        with self._lock:
            manifest["last_seen"] = datetime.now().isoformat()
            self.nodes[node_id] = manifest
            self._save_registry()
            logger.info(f"Registry updated for node: {node_id}")

    def get_node(self, node_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves info for a specific node."""
        with self._lock:
            return self.nodes.get(node_id)

    def get_nodes_by_capability(self, capability: str) -> List[str]:
        """Returns a list of node IDs that possess a specific capability (agent or hardware)."""
        with self._lock:
            return [
                nid for nid, manifest in self.nodes.items() 
                if capability in manifest.get("agents", []) or capability in manifest.get("hardware", [])
            ]

    def get_best_node_for_task(self, requirement: str) -> Optional[str]:
        """
        Simple heuristic to route tasks to the best node.
        Example: if requirement is 'high_vram', return the node with the best GPU.
        """
        with self._lock:
            if not self.nodes:
                return None
                
            if requirement == "high_vram":
                # Find node with 'GPU' in hardware and highest RAM
                gpu_nodes = [nid for nid, m in self.nodes.items() if "GPU" in m.get("hardware", [])]
                return gpu_nodes[0] if gpu_nodes else None
            
            # Default to returning a random active node or the first one
            return list(self.nodes.keys())[0]

    def _save_registry(self):
        """Persists the registry to disk."""
        try:
            os.makedirs(os.path.dirname(self.state_file), exist_ok=True)
            with open(self.state_file, "w", encoding="utf-8") as f:
                json.dump(self.nodes, f, indent=4)
        except Exception as e:
            logger.error(f"Error saving registry: {e}")

    def _load_registry(self):
        """Loads the registry from disk."""
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, "r", encoding="utf-8") as f:
                    self.nodes = json.load(f)
            except Exception as e:
                logger.error(f"Error loading registry: {e}")

# Singleton instance (will be initialized with node_id during boot)
mesh_registry = None 
