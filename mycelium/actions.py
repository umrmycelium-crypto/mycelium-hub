from .jellyfin import search_media

def execute(intent, text):
    if intent == "media.play":
        # Extract title (naively for v0)
        title = text.lower().replace("play", "").replace("watch", "").replace("start", "").strip()
        print(f"[MEDIA] Searching Jellyfin for: '{title}'")
        
        results = search_media(title)
        
        if "error" in results:
            print(f"[MEDIA] Error: {results['error']}")
        elif not results.get("Items"):
            print(f"[MEDIA] No matches found in library for: '{title}'")
        else:
            items = results["Items"]
            print(f"[MEDIA] Found {len(items)} match(es):")
            for item in items:
                print(f" - {item.get('Name')} ({item.get('Type')}) - ID: {item.get('Id')}")
            
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
