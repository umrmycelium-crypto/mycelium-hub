from mycelium.core.registry import REGISTRY


def register_intent(name: str, handler):
    """
    Safely registers new capabilities at runtime.
    """
    if name in REGISTRY:
        return {"status": "EXISTS"}

    REGISTRY[name] = handler

    return {
        "status": "REGISTERED",
        "intent": name
    }
