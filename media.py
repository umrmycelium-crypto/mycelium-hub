from mycelium.runtime.media.orchestrator import handle_media_play


def media_play(payload, context):
    title = payload.get("title", "unknown")

    return handle_media_play(title)
