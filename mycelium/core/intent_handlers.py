from mycelium.core.intent_registry import intent
from mycelium.core.media_manager import MediaManager
from mycelium.core.media_models import MediaItem
from typing import Dict, Any, List

media_manager = MediaManager()

@intent("media.search")
def handle_media_search(payload: Dict[str, Any], context: Dict[str, Any]):
    """
    Intent: Search for media across the ecosystem.
    Expected input: {"input": "find Inception"}
    """
    query = payload.get("input", "").replace("find", "").replace("search", "").strip()
    if not query:
        return {"error": "No search query provided"}
    
    results = media_manager.find_media(query)
    return {
        "status": "OK",
        "results": [item.to_dict() for item in results]
    }

@intent("media.play")
def handle_media_play(payload: Dict[str, Any], context: Dict[str, Any]):
    """
    Intent: Play media on a specific session.
    Expected input: {"item_id": "...", "session_id": "..."}
    """
    item_id = payload.get("item_id")
    session_id = payload.get("session_id")
    
    if not item_id or not session_id:
        return {"error": "item_id and session_id are required for playback"}
    
    # We create a dummy MediaItem to pass to the manager
    item = MediaItem(title="Unknown", media_type=None, id=item_id)
    res = media_manager.play_media(item, session_id)
    
    return {
        "status": "OK" if res == 204 else "ERROR",
        "status_code": res
    }

@intent("media.status")
def handle_media_status(payload: Dict[str, Any], context: Dict[str, Any]):
    """
    Intent: Check the status of a requested item.
    Expected input: {"external_id": "tmdb_id"}
    """
    ext_id = payload.get("external_id")
    if not ext_id:
        return {"error": "external_id is required to track status"}
    
    status = media_manager.track_request(ext_id)
    return {
        "status": "OK",
        "media_status": status
    }

@intent("system.status")
def handle_system_status(payload: Dict[str, Any], context: Dict[str, Any]):
    return {
        "status": "OK",
        "system": "Mycelium Core",
        "health": "Healthy",
        "phase": "Phase 3 - Intent Engine"
    }
