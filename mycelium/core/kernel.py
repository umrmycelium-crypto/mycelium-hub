import threading
import time
import logging
import os
import socket
from typing import Any, Dict, Optional
from mycelium.core.distributed_bus import DistributedBus, SystemEvent
from mycelium.core.cognitive_state import cognitive_state
from mycelium.core.intent_engine import engine as intent_engine
from mycelium.core.dispatcher import dispatcher
from mycelium.core.mesh_registry import MeshRegistry
from mycelium.core.mesh_state import MeshState
from mycelium.core.capability_router import CapabilityRouter

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(name)s: %(message)s')

class MyceliumKernel:
    """
    The central orchestrator of the Mycelium OS.
    Drives the proactive event loop and manages system-wide state transitions.
    """
    def __init__(self):
        self.logger = logging.getLogger("MyceliumKernel")
        self.running = False
        self._loop_thread: Optional[threading.Thread] = None
        
        # 1. Identify Node
        self.node_id = os.getenv("MYCELIUM_NODE_ID", socket.gethostname())
        
        # 2. Initialize Distributed Infrastructure
        mesh_nodes = os.getenv("MYCELIUM_MESH_NODES", "").split(",")
        mesh_nodes = [n for n in mesh_nodes if n]
        
        self.bus = DistributedBus(
            node_id=self.node_id, 
            mesh_nodes=mesh_nodes
        )
        
        # 3. Initialize Mesh Registry
        from mycelium.core.mesh_registry import MeshRegistry as RegistryClass
        self.registry = RegistryClass(node_id=self.node_id)
        
        # 4. Initialize Distributed State and Routing
        self.mesh_state = MeshState(bus=self.bus)
        self.router = CapabilityRouter(registry=self.registry)
        
        # Subscribe the kernel to all events to drive the cognitive loop
        self.bus.subscribe("*", self._on_system_event)

    def start(self):
        """Boots the kernel and starts the event loop."""
        self.logger.info(f"Mycelium Kernel Booting on Node: {self.node_id}...")
        
        # Announce presence to the mesh
        self._announce_presence()
        
        self.running = True
        self._loop_thread = threading.Thread(target=self._main_loop, daemon=True)
        self._loop_thread.start()
        self.logger.info("Mycelium Kernel Online. Distributed event loop active.")

    def stop(self):
        """Shuts down the kernel."""
        self.running = False
        if self._loop_thread:
            self._loop_thread.join()
        self.logger.info("Mycelium Kernel Shutdown.")

    def _announce_presence(self):
        """Publishes a node announcement event so others can map the mesh."""
        manifest = {
            "os": "Linux", # Simplified for now
            "hardware": ["CPU", "GPU", "RAM"], # Simplified
            "agents": ["MediaAgent", "KnowledgeAgent", "DevelopmentAgent", "SystemAgent"]
        }
        
        event = SystemEvent(
            type="node.announcement",
            payload={"manifest": manifest, "node_id": self.node_id},
            source=self.node_id,
            priority=1
        )
        self.bus.publish(event, global_broadcast=True)
        
        # Update local registry
        self.registry.update_node(self.node_id, manifest)

    def _on_system_event(self, event: SystemEvent):
        """
        Callback for every event on the bus.
        Updates cognitive state and evaluates if a proactive action is needed.
        """
        self.logger.info(f"Kernel processing event: {event.type} | Source: {event.source}")
        
        # 1. Update Cognitive State
        cognitive_state.add_event(event.type, event.payload)
        
        # 2. Mesh Registry Update: If it's an announcement, map the node
        if event.type == "node.announcement":
            node_id = event.payload.get("node_id")
            manifest = event.payload.get("manifest")
            if node_id and manifest:
                self.registry.update_node(node_id, manifest)

        # 3. Evaluate for Proactivity
        if event.type == "user.presence" and event.payload.get("status") == "PRESENT":
            self._trigger_proactive_greeting()

    def _trigger_proactive_greeting(self):
        """Example proactive action: Greet the user when they return."""
        self.logger.info("Triggering proactive greeting sequence...")
        intent_text = "Greet the user and suggest a movie based on their current mood and history."
        threading.Thread(target=lambda: intent_engine.process(intent_text)).start()

    def _main_loop(self):
        """
        The heartbeat of the OS. 
        """
        while self.running:
            try:
                time.sleep(1) 
            except Exception as e:
                self.logger.error(f"Kernel loop error: {e}")

# Singleton instance
kernel = MyceliumKernel()
