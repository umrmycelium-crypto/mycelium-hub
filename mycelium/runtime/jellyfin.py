import requests

JELLYFIN_URL = "http://10.0.0.221:8096"
API_KEY = "8cde02ba7f1a43cfb76209ccfc4c708f"  # move to .env later


def search_media(query: str):
    url = f"{JELLYFIN_URL}/Items"
    headers = {"X-Emby-Token": API_KEY}

    params = {
        "SearchTerm": query,
        "IncludeItemTypes": "Movie",
        "Limit": 1
    }

    r = requests.get(url, headers=headers, params=params)

    data = r.json()

    items = data.get("Items", [])
    if not items:
        return None

    return items[0]


def get_active_session():
    url = f"{JELLYFIN_URL}/Sessions"
    headers = {"X-Emby-Token": API_KEY}

    r = requests.get(url, headers=headers)
    sessions = r.json()

    for s in sessions:
        if s.get("NowPlayingItem"):
            return s

    # fallback: first controllable device
    return sessions[0] if sessions else None


def play_on_device(item):
    session = get_active_session()

    if not session:
        return {"status": "NO_SESSION"}

    session_id = session["Id"]
    item_id = item["Id"]

    url = f"{JELLYFIN_URL}/Sessions/{session_id}/Playing"

    headers = {"X-Emby-Token": API_KEY}

    payload = {
        "ItemIds": [item_id]
    }

    r = requests.post(url, headers=headers, json=payload)

    return {
        "session": session.get("DeviceName", "unknown"),
        "item": item.get("Name"),
        "status_code": r.status_code
    }
