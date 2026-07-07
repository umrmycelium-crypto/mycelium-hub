from typing import Any, Dict, List, Optional
from mycelium.core.mesh_registry import MeshRegistry

class CapabilityRouter:
    """
    The Capability Router optimizes task allocation across the Mycelium Mesh.
    It routes tasks to the node best equipped to handle them based on the Node Manifest.
    """
    def __init__(self, registry: MeshRegistry):
        self.registry = registry

    def route_task(self, requirement: str, payload: Dict[str, Any]) -> Optional[str]:
        """
        Determines the best node ID for a given requirement.
        Examples: 'high_vram', 'low_latency', 'storage_heavy'.
        """
        node_id = self.registry.get_best_node_for_task(requirement)
        
        if not node_id:
            return None
            
        return node_id

    def resolve_execution_node(self, task_type: str) -> str:
        """
        Maps specific task types to optimal nodes.
        """
        if task_type == "rendering":
            # Always route rendering to The Studio
            return self.registry.get_best_node_for_task("high_vram")
        
        if task_type == "knowledge_synthesis":
            # Route to the node with the most stable connection to the vault
            return self.registry.get_best_node_for_task("storage_heavy")
            
        # Default to current local node
        return "local"

# Singleton will be initialized in the kernel
capability_router = None
