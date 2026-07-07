from mycelium.core.registry import REGISTRY
from mycelium.core.kernel import execute
from mycelium.core.cortex_runtime.resilient_compile import safe_compile


def run(user_input: str):
    """
    Runtime orchestration layer (OS kernel boundary)
    """

    registry_keys = list(REGISTRY.keys())

    # 1. Compile intent (Cortex)
    intent_graph = safe_compile(user_input, registry_keys)

    if not intent_graph.get("intents"):
        return {
            "status": "NO_INTENT",
            "input": user_input
        }

    results = []

    # 2. Execute each intent via kernel
    for intent in intent_graph["intents"]:

        intent_obj = type("Intent", (), {
            "name": intent["name"],
            "confidence": intent["confidence"],
            "payload": intent.get("payload", {}),
            "context": {"source": "runtime.entry"}
        })()

        result = execute(intent_obj)
        results.append(result)

    # 3. Return normalized output
    return {
        "status": "OK",
        "results": results
    }
