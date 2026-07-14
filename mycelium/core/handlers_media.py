from mycelium.core.registry_decorator import register
from mycelium.runtime.media.orchestrator import handle_media_play as media_play_runtime

@register("media.play")
def media_play(payload, context):
    return media_play_runtime(payload, context)
