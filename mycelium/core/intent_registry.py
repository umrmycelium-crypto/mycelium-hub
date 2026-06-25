"""
Decorator-based intent registry
Replaces manual REGISTRY dict.
"""

from collections import defaultdict

REGISTRY = {}


def intent(name: str):
    """
    Decorator to register intent handlers.
    """

    def wrapper(fn):
        REGISTRY[name] = fn
        return fn

    return wrapper


def get_registry():
    return REGISTRY
