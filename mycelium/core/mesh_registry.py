import json
import os
import threading
import logging
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MeshRegistry")

class MeshRegistry:
    """
    The MeshRegistry tracks the topography and real-time status of the Mycelium network.
    It maintains a map of active nodes, hardware, OS platforms, and active capabilities.
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
            now_iso = datetime.now(timezone.utc).isoformat()
            if node_id in self.nodes:
                self.nodes[node_id].update(manifest)
                self.nodes[node_id]["last_seen"] = now_iso
            else:
                manifest["last_seen"] = now_iso
                manifest["registered_at"] = now_iso
                self.nodes[node_id] = manifest
            self._save_registry()
            logger.info(f"Registry updated for node: {node_id}")

    def heartbeat_node(self, node_id: str):
        """Records a heartbeat pulse for an active node."""
        with self._lock:
            if node_id in self.nodes:
                self.nodes[node_id]["last_seen"] = datetime.now(timezone.utc).isoformat()
                self._save_registry()

    def prune_stale_nodes(self, timeout_seconds: float = 60.0) -> List[str]:
        """Prunes nodes that haven't sent a heartbeat within the timeout period."""
        pruned: List[str] = []
        now = datetime.now(timezone.utc)
        with self._lock:
            for nid, manifest in list(self.nodes.items()):
                if nid == self.node_id:
                    continue  # Never prune self
                last_seen_str = manifest.get("last_seen")
                if not last_seen_str:
                    continue
                try:
                    last_seen = datetime.fromisoformat(last_seen_str)
                    if (now - last_seen).total_seconds() > timeout_seconds:
                        del self.nodes[nid]
                        pruned.append(nid)
                except Exception:
                    pass
            if pruned:
                self._save_registry()
                logger.info(f"Pruned stale nodes from mesh: {pruned}")
        return pruned

    def get_node(self, node_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves info for a specific node."""
        with self._lock:
            return self.nodes.get(node_id)

    def get_nodes_by_capability(self, capability: str) -> List[str]:
        """Returns a list of node IDs that possess a specific capability or role."""
        with self._lock:
            return [
                nid for nid, manifest in self.nodes.items() 
                if capability in manifest.get("agents", []) 
                or capability in manifest.get("hardware", [])
                or capability.lower() == manifest.get("os", "").lower()
            ]

    def get_best_node_for_task(self, requirement: str) -> Optional[str]:
        """
        Heuristic capability router to allocate tasks across the mesh.
        """
        with self._lock:
            if not self.nodes:
                return self.node_id
                
            if requirement == "high_vram":
                gpu_nodes = [nid for nid, m in self.nodes.items() if "GPU" in m.get("hardware", [])]
                if gpu_nodes:
                    return gpu_nodes[0]
            
            if requirement == "storage_heavy":
                storage_nodes = [nid for nid, m in self.nodes.items() if "Storage" in m.get("hardware", []) or "NAS" in m.get("hardware", [])]
                if storage_nodes:
                    return storage_nodes[0]

            if requirement in ["windows", "win32"]:
                win_nodes = [nid for nid, m in self.nodes.items() if m.get("os", "").lower() in ["windows", "win32"]]
                if win_nodes:
                    return win_nodes[0]

            if requirement in ["darwin", "mac", "macos"]:
                mac_nodes = [nid for nid, m in self.nodes.items() if m.get("os", "").lower() in ["darwin", "mac", "macos"]]
                if mac_nodes:
                    return mac_nodes[0]

            # Match capability by agent or hardware
            matching = [
                nid for nid, m in self.nodes.items()
                if requirement in m.get("agents", []) or requirement in m.get("hardware", [])
            ]
            if matching:
                return matching[0]
            
            # Default to self or first registered node
            return self.node_id if self.node_id in self.nodes else list(self.nodes.keys())[0]

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

# Global instance initialization placeholder
mesh_registry = None
 
