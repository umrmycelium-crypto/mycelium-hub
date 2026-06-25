from mycelium.core.registry_decorator import register
from mycelium.runtime.ai import ai_ask as ai_ask_runtime

@register("ai.ask")
def ai_ask(payload, context):
    return ai_ask_runtime(payload, context)
