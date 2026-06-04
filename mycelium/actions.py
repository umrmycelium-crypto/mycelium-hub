from .jellyfin import search_media, get_sessions, play_media

def execute(intent, text):
    if intent == "media.play":
        # Extract title (naively for v0)
        title = text.lower().replace("play", "").replace("watch", "").replace("start", "").strip()
        print(f"[MEDIA] Searching Jellyfin for: '{title}'")
        
        results = search_media(title)
        
        if "error" in results:
            print(f"[MEDIA] Error searching media: {results['error']}")
            return
            
        if not results.get("Items"):
            print(f"[MEDIA] No matches found in library for: '{title}'")
            return

        item = results["Items"][0]
        item_id = item["Id"]
        print(f"[MEDIA] Selected: {item.get('Name')} ({item.get('Type')})")

        # Find active session (prefer Samsung TV)
        sessions = get_sessions()
        if "error" in sessions:
            print(f"[MEDIA] Error retrieving sessions: {sessions['error']}")
            return

        tv_session_id = None
        for s in sessions:
            if "Samsung" in s.get("DeviceName", ""):
                tv_session_id = s["Id"]
                print(f"[MEDIA] Target device found: {s.get('DeviceName')}")
                break
        
        if not tv_session_id:
            print("[MEDIA] No active Samsung TV session found. Check if the app is open.")
            return

        status = play_media(tv_session_id, item_id)
        print(f"[MEDIA] Playback response status: {status}")
            
    elif intent == "media.search":
        print(f"[MEDIA] Action: Searching for: '{text}'")
    elif intent == "system.status":
        print("[SYSTEM] Action: Retrieving system health and service status.")
    elif intent == "knowledge.search":
        print(f"[KNOWLEDGE] Action: Searching Obsidian vault for: '{text}'")
    elif intent == "developer.assist":
        print(f"[DEV] Action: Invoking Gemini CLI for: '{text}'")
    else:
        print(f"[UNKNOWN] No action mapped for intent: {intent}")
