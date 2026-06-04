def execute(intent, text):
    if intent == "media.play":
        print(f"[MEDIA] Action: Play matching content for: '{text}'")
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
