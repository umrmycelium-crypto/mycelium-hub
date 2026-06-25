class Registry(dict):
    """
    Minimal stable registry core for Mycelium runtime.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # Decorator-driven handler registration.
    def register(self, name: str, fn):
        self[name] = fn
        return fn


# singleton accessor (safe fallback pattern)
_registry = Registry()

def get_registry():
    return _registry
