from .jellyfin import search_media, get_sessions, play_media
from .gemini_executor import run_gemini_command
from .knowledge import search_notes

def execute(intent, text):
    if intent == "media.play":
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

    elif intent == "developer.assist":
        print(f"[DEV] Analyzing request with Gemini CLI...")
        prompt = f"Analyze the following Mycelium Ecosystem request and provide a brief technical assessment: '{text}'"
        response = run_gemini_command(prompt)
        print("-" * 20)
        print(response)
        print("-" * 20)

    elif intent == "system.status":
        print("[SYSTEM] Action: Retrieving system health and service status.")

    elif intent == "knowledge.search":
        # More aggressive query extraction for v0
        query = text.lower()
        stop_phrases = ["what did i write about", "what did i say about", "search for", "find in vault", "note down", "remember"]
        for phrase in stop_phrases:
            query = query.replace(phrase, "")
        
        # Also remove individual keywords
        for kw in ["note", "search", "remember", "find", "about", "vault", "thought"]:
            query = query.replace(kw, "")
            
        query = query.strip()
        print(f"[KNOWLEDGE] Searching vault for: '{query}'")
        
        results = search_notes(query)
        
        if isinstance(results, dict) and "error" in results:
            print(f"[KNOWLEDGE] Error: {results['error']}")
        elif not results:
            print(f"[KNOWLEDGE] No notes found matching: '{query}'")
        else:
            print(f"[KNOWLEDGE] Found {len(results)} matching note(s):")
            for rel_path in results:
                print(f" - {rel_path}")

    else:
        print(f"[UNKNOWN] No action mapped for intent: {intent}")
