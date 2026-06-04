import requests
import os
from dotenv import load_dotenv

load_dotenv()

SERVER = os.getenv("JELLYSEERR_SERVER", "http://10.0.0.221:5055/api/v1")
API_KEY = os.getenv("JELLYSEERR_API_KEY")

HEADERS = {
    "X-Api-Key": API_KEY,
    "Content-Type": "application/json"
}

def search_media(query):
    """
    Searches Jellyseerr (via TMDB) for media to request.
    """
    if not API_KEY:
        return {"error": "Jellyseerr API Key not configured"}

    url = f"{SERVER}/search"
    params = {"query": query}
    
    try:
        r = requests.get(url, headers=HEADERS, params=params, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"error": str(e)}

def request_media(tmdb_id, media_type="movie"):
    """
    Submits a request to Jellyseerr.
    """
    if not API_KEY:
        return {"error": "Jellyseerr API Key not configured"}

    url = f"{SERVER}/request"
    payload = {
        "mediaType": media_type,
        "mediaId": tmdb_id
    }
    
    try:
        r = requests.post(url, headers=HEADERS, json=payload, timeout=10)
        return r.json()
    except Exception as e:
        return {"error": str(e)}

def get_requests():
    """
    Retrieves the list of active requests from Jellyseerr.
    """
    if not API_KEY:
        return {"error": "Jellyseerr API Key not configured"}

    url = f"{SERVER}/request"
    params = {"take": 10, "skip": 0, "filter": "all"}
    
    try:
        r = requests.get(url, headers=HEADERS, params=params, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"error": str(e)}
