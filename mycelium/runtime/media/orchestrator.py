from mycelium.runtime.jellyfin import search_media, play_on_device
from mycelium.runtime.jellyseerr import request_media


def handle_media_play(payload, context):
    title = payload.get("title", "")
    # 1. Try Jellyfin first
    item = search_media(title)

    if item:
        return play_on_device(item)

    # 2. If not found → request pipeline
    request_result = request_media(title)

    return {
        "status": "PENDING",
        "action": "media.request_download",
        "title": title,
        "message": "Not found. Request submitted to acquisition system.",
        "request": request_result
    }
