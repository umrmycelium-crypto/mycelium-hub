from mycelium.core.registry_core import get_registry

def route(intent: dict):
    name = intent.get("name")

    handler = get_registry().get(name)

    if not handler:
        return {"status": "NO_HANDLER", "intent": name}

    return handler(intent.get("payload", {}), intent.get("context", {}))
