from .jellyfin import search_media, get_sessions, play_media
from .gemini_executor import run_gemini_command
from .knowledge import search_notes
from .core.response import make_response

def handle_media_play(payload):
    intent = "media.play"
    # Prioritize extracted title from LLM entities
    title = payload.get("title")
    if not title:
        text = payload.get("text", "")
        title = text.lower().replace("play", "").replace("watch", "").replace("start", "").strip()
    
    print(f"[MEDIA] Searching Jellyfin for: '{title}'")
    results = search_media(title)
    if "error" in results:
        return make_response(intent, "error", message=f"Error searching media: {results['error']}")
    if not results.get("Items"):
        return make_response(intent, "not_found", message=f"No matches found in library for: '{title}'")

    item = results["Items"][0]
    item_id = item["Id"]
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
        message="System is operational. Services: Jellyfin, Ollama, Gemini CLI."
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
