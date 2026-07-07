import json
import socket
import threading
import logging
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime

# Use the same event schema as the local bus
from mycelium.core.nervous_bus import SystemEvent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("DistributedBus")

class DistributedBus:
    """
    The networked version of the NervousBus.
    Allows events to be broadcast across the Mycelium Mesh using a TCP-based 
    distribution model.
    """
    def __init__(self, node_id: str, port: int = 5555, mesh_nodes: List[str] = None):
        self.node_id = node_id
        self.port = port
        self.mesh_nodes = mesh_nodes or []
        self._subscribers: Dict[str, List[Callable]] = {}
        self._lock = threading.Lock()
        
        # Start the listener thread to receive events from other nodes
        self._stop_event = threading.Event()
        self._listener_thread = threading.Thread(target=self._listen, daemon=True)
        self._listener_thread.start()

    def subscribe(self, event_type: str, callback: Callable):
        """Registers a callback for a specific event type."""
        with self._lock:
            if event_type not in self._subscribers:
                self._subscribers[event_type] = []
            self._subscribers[event_type].append(callback)

    def publish(self, event: SystemEvent, global_broadcast: bool = False):
        """
        Publishes an event.
        If global_broadcast is True, it sends the event to all other nodes in the mesh.
        """
        # 1. Local delivery
        self._deliver_local(event)
        
        # 2. Global delivery
        if global_broadcast:
            self._broadcast(event)

    def _deliver_local(self, event: SystemEvent):
        """Internal method to trigger local subscribers."""
        with self._lock:
            callbacks = self._subscribers.get(event.type, []).copy()
            callbacks.extend(self._subscribers.get("*", []))

        for callback in callbacks:
            try:
                callback(event)
            except Exception as e:
                logger.error(f"Error in local subscriber for event {event.type}: {e}")

    def _broadcast(self, event: SystemEvent):
        """Sends the event to all known nodes in the mesh."""
        event_data = json.dumps({
            "event": {
                "type": event.type,
                "payload": event.payload,
                "priority": event.priority,
                "timestamp": event.timestamp,
                "source": event.source
            },
            "origin_node": self.node_id
        })
        
        for node_ip in self.mesh_nodes:
            if node_ip == socket.gethostname(): # Skip self if hostname is in list
                continue
            
            threading.Thread(target=self._send_to_node, args=(node_ip, event_data), daemon=True).start()

    def _send_to_node(self, ip: str, data: str):
        """TCP sender for a single node."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(2.0)
                s.connect((ip, self.port))
                s.sendall(data.encode('utf-8'))
        except Exception as e:
            logger.debug(f"Could not send event to node {ip}: {e}")

    def _listen(self):
        """Server loop to receive events from the mesh."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('0.0.0.0', self.port))
            s.listen()
            while not self._stop_event.is_set():
                try:
                    conn, addr = s.accept()
                    with conn:
                        data = conn.recv(4096).decode('utf-8')
                        if data:
                            self._handle_incoming(data)
                except Exception as e:
                    logger.error(f"Listener error: {e}")

    def _handle_incoming(self, data: str):
        """Parses incoming network data back into a SystemEvent."""
        try:
            msg = json.loads(data)
            event_dict = msg["event"]
            
            event = SystemEvent(
                type=event_dict["type"],
                payload=event_dict["payload"],
                priority=event_dict["priority"],
                timestamp=event_dict["timestamp"],
                source=event_dict["source"]
            )
            # Mark that this event came from the network
            event.source = f"{event.source} (via {msg['origin_node']})"
            
            self._deliver_local(event)
        except Exception as e:
            logger.error(f"Error parsing incoming event: {e}")

    def stop(self):
        self._stop_event.set()
