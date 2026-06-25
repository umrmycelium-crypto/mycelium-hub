import re


def extract_title(text: str):
    # remove command verbs
    text = re.sub(r"^(play|start|watch|run)\s+", "", text.strip(), flags=re.IGNORECASE)
    return text.strip() or "unknown"


def safe_compile(user_input, registry_keys):
    intents = []

    text = user_input.lower().strip()

    # MEDIA INTENT
    if any(x in text for x in ["play", "watch", "start movie"]):
        intents.append({
            "name": "media.play",
            "confidence": 0.9,
            "payload": {
                "title": extract_title(user_input)
            }
        })
        return {"intents": intents}

    # SYSTEM INTENTS
    if "ping" in text:
        intents.append({
            "name": "system.ping",
            "confidence": 0.95,
            "payload": {}
        })
        return {"intents": intents}

    if "status" in text:
        intents.append({
            "name": "system.status",
            "confidence": 0.95,
            "payload": {}
        })
        return {"intents": intents}

    return {"intents": []}
