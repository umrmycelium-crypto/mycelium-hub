import requests
import os
from dotenv import load_dotenv

load_dotenv()

SERVER = os.getenv("JELLYFIN_SERVER", "http://10.0.0.221:8096")
API_KEY = os.getenv("JELLYFIN_API_KEY")

HEADERS = {
    "X-Emby-Token": API_KEY,
    "Content-Type": "application/json"
}

def search_media(query):
    if not API_KEY:
        return {"error": "Jellyfin API Key not configured"}

    url = f"{SERVER}/Items"
    params = {
        "searchTerm": query,
        "Recursive": True,
        "IncludeItemTypes": "Movie,Series,Episode",
        "Limit": 5
    }

    try:
        r = requests.get(
            url,
            headers=HEADERS,
            params=params,
            timeout=10
        )
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"error": str(e)}

def get_active_sessions():
    if not API_KEY:
        return {"error": "Jellyfin API Key not configured"}

    url = f"{SERVER}/Sessions"
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"error": str(e)}
