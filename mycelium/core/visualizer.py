from mycelium.core.execution_trace import trace
from mycelium.core.registry_core import get_registry


def visualize_registry():
    registry = get_registry()

    return {
        "registered_intents": list(registry.keys()),
        "count": len(registry)
    }


def visualize_execution(intent_name: str, result: dict):
    trace("intent.executed", {
        "intent": intent_name,
        "result": result
    })

    return result


def system_visualize(payload, context):
    return {
        "registry": visualize_registry()
    }
