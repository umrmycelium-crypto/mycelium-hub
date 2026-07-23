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
    distribution model with SO_REUSEADDR and auto-reconnection.
    """
    def __init__(self, node_id: str, port: int = 5555, mesh_nodes: List[str] = None):
        self.node_id = node_id
        self.port = port
        self.mesh_nodes = mesh_nodes or []
        self._subscribers: Dict[str, List[Callable]] = {}
        self._lock = threading.Lock()
        
        # Listener control
        self._stop_event = threading.Event()
        self._server_socket: Optional[socket.socket] = None
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
        If global_broadcast is True, sends the event to all remote nodes in the mesh.
        """
        # 1. Local delivery
        self._deliver_local(event)
        
        # 2. Global delivery
        if global_broadcast and self.mesh_nodes:
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
        
        hostname = socket.gethostname()
        for node_ip in self.mesh_nodes:
            if node_ip in [hostname, "127.0.0.1", "localhost"] and self.port == 5555:
                continue
            
            threading.Thread(target=self._send_to_node, args=(node_ip, event_data), daemon=True).start()

    def _send_to_node(self, ip: str, data: str):
        """TCP sender for a single node."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(3.0)
                s.connect((ip, self.port))
                s.sendall(data.encode('utf-8'))
        except Exception as e:
            logger.debug(f"Could not send event to node {ip}:{self.port}: {e}")

    def _listen(self):
        """Server loop to receive events from the mesh."""
        try:
            self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self._server_socket.bind(('0.0.0.0', self.port))
            self._server_socket.listen(5)
            self._server_socket.settimeout(1.0)
            
            while not self._stop_event.is_set():
                try:
                    conn, addr = self._server_socket.accept()
                    with conn:
                        conn.settimeout(3.0)
                        data = conn.recv(16384).decode('utf-8')
                        if data:
                            self._handle_incoming(data)
                except socket.timeout:
                    continue
                except Exception as e:
                    if not self._stop_event.is_set():
                        logger.error(f"Listener error: {e}")
        except Exception as e:
            logger.error(f"Could not start DistributedBus server socket on port {self.port}: {e}")
        finally:
            if self._server_socket:
                try:
                    self._server_socket.close()
                except Exception:
                    pass

    def _handle_incoming(self, data: str):
        """Parses incoming network data into a SystemEvent."""
        try:
            msg = json.loads(data)
            event_dict = msg["event"]
            
            event = SystemEvent(
                type=event_dict["type"],
                payload=event_dict["payload"],
                priority=event_dict["priority"],
                timestamp=event_dict["timestamp"],
                source=f"{event_dict['source']} (via {msg.get('origin_node', 'unknown')})"
            )
            
            self._deliver_local(event)
        except Exception as e:
            logger.error(f"Error parsing incoming event: {e}")

    def stop(self):
        self._stop_event.set()
        if self._server_socket:
            try:
                self._server_socket.close()
            except Exception:
                pass

