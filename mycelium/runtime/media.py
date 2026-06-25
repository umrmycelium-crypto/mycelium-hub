from mycelium.runtime.jellyfin import search_media, play_on_device
from mycelium.runtime.acquisition import request_acquisition


def media_play(payload, context):
    title = payload.get("title", "unknown")

    # 1. Search library
    item = search_media(title)

    if not item:
        return request_acquisition(title)

    # 2. CRITICAL FIX: ensure mediaId exists
    media_id = item.get("Id") or item.get("mediaId")

    if not media_id:
        return {
            "status": "ERROR",
            "action": "media.play",
            "title": title,
            "message": "Media found but missing mediaId",
            "debug_item": item
        }

    # 3. Play using proper Jellyfin contract
    result = play_on_device(media_id)

    return {
        "status": "OK",
        "action": "media.play",
        "title": item.get("Name", title),
        "message": "Playback triggered",
        "mediaId": media_id,
        "session_result": result
    }
