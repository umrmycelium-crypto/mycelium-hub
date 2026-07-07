from typing import Any, Callable, Dict, List
from dataclasses import dataclass, field
from datetime import datetime
import threading
import logging

@dataclass
class SystemEvent:
    """
    A standardized event within the Mycelium Ecosystem.
    """
    type: str
    payload: Dict[str, Any] = field(default_factory=dict)
    priority: int = 0  # Higher is more urgent
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    source: str = "system"

class NervousBus:
    """
    The central event bus for the Mycelium OS.
    Allows components to publish events and subscribe to specific event types.
    """
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}
        self._lock = threading.Lock()
        self.logger = logging.getLogger("NervousBus")

    def subscribe(self, event_type: str, callback: Callable):
        """Registers a callback for a specific event type."""
        with self._lock:
            if event_type not in self._subscribers:
                self._subscribers[event_type] = []
            self._subscribers[event_type].append(callback)
            self.logger.info(f"Subscribed to {event_type}: {callback.__name__ if hasattr(callback, '__name__') else 'anonymous'}")

    def publish(self, event: SystemEvent):
        """Publishes an event to all registered subscribers."""
        self.logger.info(f"Event Published: {event.type} | Source: {event.source}")
        
        # Notify specific subscribers
        with self._lock:
            callbacks = self._subscribers.get(event.type, []).copy()
            # Also notify global subscribers (listening to '*')
            callbacks.extend(self._subscribers.get("*", []))

        for callback in callbacks:
            try:
                callback(event)
            except Exception as e:
                self.logger.error(f"Error in subscriber {callback} for event {event.type}: {e}")

# Singleton instance
nervous_bus = NervousBus()
