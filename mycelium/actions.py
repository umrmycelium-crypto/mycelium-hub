from .jellyfin import search_media, get_sessions, play_media
from .jellyseerr import search_media as search_jellyseerr, request_media
from .gemini_executor import run_gemini_command
from .knowledge import search_notes
from .core.response import make_response

def handle_media_play(payload):
    intent = "media.play"
    title = payload.get("title")
    if not title:
        text = payload.get("text", "")
        title = text.lower().replace("play", "").replace("watch", "").replace("start", "").strip()
    
    print(f"[MEDIA] Searching Jellyfin for: '{title}'")
    results = search_media(title)
    
    if results.get("Items"):
        item = results["Items"][0]
        item_id = item["Id"]
        print(f"[MEDIA] Selected: {item.get('Name')} ({item.get('Type')})")

        sessions = get_sessions()
        if "error" in sessions:
            return make_response(intent, "error", message=f"Error retrieving sessions: {sessions['error']}")

        tv_session_id = None
        target_device = "Unknown"
        for s in sessions:
            if "Samsung" in s.get("DeviceName", ""):
                tv_session_id = s["Id"]
                target_device = s.get("DeviceName")
                break
        
        if not tv_session_id:
            return make_response(intent, "device_offline", message="No active Samsung TV session found. Check if the app is open.")

        status_code = play_media(tv_session_id, item_id)
        return make_response(
            intent=intent,
            status="success" if status_code == 204 else "failed",
            data={"title": item.get('Name'), "id": item_id, "device": target_device},
            message=f"Playing {item.get('Name')} on {target_device}",
            debug={"status_code": status_code}
        )

    # Content missing: Auto-trigger download request
    print(f"[MEDIA] Not found in library. Emitting auto-request for: '{title}'")
    return handle_media_request({"query": title, "text": payload.get("text")})

def handle_media_request(payload):
    query = payload.get("query") or payload.get("title")
    intent = "media.request_download"
    print(f"[MEDIA] Searching Jellyseerr for: '{query}'")
    
    search_results = search_jellyseerr(query)
    if "error" in search_results:
        return make_response(intent, "error", message=f"Jellyseerr error: {search_results['error']}")
    
    results = search_results.get("results", [])
    if not results:
        return make_response(intent, "not_found", message=f"No matches found on TMDB for: '{query}'")
    
    best_match = results[0]
    tmdb_id = best_match.get("id")
    media_type = best_match.get("mediaType", "movie")
    
    match_title = best_match.get('title') or best_match.get('name')
    print(f"[MEDIA] Requesting '{match_title}' via Jellyseerr...")
    request_result = request_media(tmdb_id, media_type)
    
    if "error" in request_result:
        return make_response(intent, "error", message=f"Request failed: {request_result['error']}")
        
    return make_response(
        intent=intent,
        status="success",
        data={"title": match_title, "tmdbId": tmdb_id},
        message=f"Request submitted for '{match_title}'. It will be available for playback soon."
    )

def handle_media_search(payload):
    intent = "media.search"
    query = payload.get("query")
    if not query:
        text = payload.get("text", "")
        query = text.lower().replace("search", "").replace("find", "").strip()
    
    results = search_media(query)
    items = results.get("Items", [])
    return make_response(
        intent=intent,
        data={"count": len(items), "results": items},
        message=f"Found {len(items)} match(es) for '{query}'"
    )

def handle_dev_assist(payload):
    text = payload.get("text", "")
    prompt = f"Analyze the following Mycelium Ecosystem request and provide a brief technical assessment: '{text}'"
    response = run_gemini_command(prompt)
    return make_response(
        intent="developer.assist",
        data={"analysis": response},
        message="Technical assessment complete."
    )

def handle_system_status(payload):
    return make_response(
        intent="system.status",
        message="System is operational. Services: Jellyfin, Ollama, Gemini CLI, Jellyseerr."
    )

def handle_knowledge_search(payload):
    intent = "knowledge.search"
    query = payload.get("query")
    if not query:
        text = payload.get("text", "")
        stop_phrases = ["what did i write about", "what did i say about", "search for", "find in vault", "note down", "remember"]
        for phrase in stop_phrases:
            text = text.replace(phrase, "")
        for kw in ["note", "search", "remember", "find", "about", "vault", "thought"]:
            text = text.replace(kw, "")
        query = text.strip()
    
    print(f"[KNOWLEDGE] Searching vault for: '{query}'")
    results = search_notes(query)
    if isinstance(results, dict) and "error" in results:
        return make_response(intent, "error", message=f"Knowledge search error: {results['error']}")
    
    return make_response(
        intent=intent,
        data={"matches": results},
        message=f"Found {len(results)} matching note(s) for '{query}'"
    )

def handle_unknown(payload):
    return make_response("unknown", "unknown", message=f"No action mapped for input: {payload.get('text')}")
