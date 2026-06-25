from mycelium.core.registry_core import get_registry

def register(name: str):
    """
    Explicit registration decorator.
    NO side effects except registry insertion.
    """

    def wrapper(fn):
        get_registry().register(name, fn)
        return fn

    return wrapper
