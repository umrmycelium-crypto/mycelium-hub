import json
import logging
from typing import Any, Dict, Optional
from mycelium.core.distributed_bus import DistributedBus, SystemEvent
from mycelium.core.nervous_bus import nervous_bus # For local fallback

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MeshState")

class MeshState:
    """
    Manages global state synchronization across the Mycelium Mesh.
    Ensures that critical facts (e.g., 'User is in the living room') are 
    consistent across all nodes.
    """
    def __init__(self, bus: DistributedBus):
        self.bus = bus
        self.global_facts: Dict[str, Any] = {}
        
        # Subscribe to state update events from other nodes
        self.bus.subscribe("state.update", self._handle_state_update)

    def update_global_fact(self, key: str, value: Any):
        """Updates a fact locally and broadcasts the change to the mesh."""
        self.global_facts[key] = value
        
        # Broadcast the update to the rest of the mesh
        event = SystemEvent(
            type="state.update",
            payload={"key": key, "value": value},
            source="mesh_state_manager",
            priority=2
        )
        self.bus.publish(event, global_broadcast=True)
        logger.info(f"Global Fact Broadcast: {key} = {value}")

    def get_global_fact(self, key: str, default: Any = None) -> Any:
        """Retrieves a fact from the global synchronized state."""
        return self.global_facts.get(key, default)

    def _handle_state_update(self, event: SystemEvent):
        """Updates local state when a broadcast is received from another node."""
        payload = event.payload
        key = payload.get("key")
        value = payload.get("value")
        
        if key:
            self.global_facts[key] = value
            logger.debug(f"Synchronized global fact: {key} = {value}")

# Singleton will be initialized in the kernel using the distributed bus
mesh_state = None
