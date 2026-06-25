from mycelium.core.self_model import update_node, add_edge
from mycelium.core.event_bus import EVENT_BUS


def install_perception_layer():

    original_emit = EVENT_BUS.emit

    def wrapped(event_type, payload=None, *args, **kwargs):

        result = original_emit(event_type, payload, *args, **kwargs)

        # ---- PERCEPTION RULES ----

        # 1. event becomes a node update
        update_node("event_bus.last_event", {
            "type": event_type,
            "payload": payload
        })

        # 2. structural interpretation
        update_node(f"event_type.{event_type}", {
            "seen": True
        })

        # 3. causal edge (event → system state)
        add_edge("event_bus", event_type, "emits")

        return result

    EVENT_BUS.emit = wrapped
