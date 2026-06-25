from mycelium.core.registry import REGISTRY


def register(name: str):
    def wrapper(fn):
        REGISTRY[name] = fn
        return fn
    return wrapper
