import requests
import os
from dotenv import load_dotenv

load_dotenv()

SERVER = os.getenv("SONARR_SERVER", "http://10.0.0.221:8989")
API_KEY = os.getenv("SONARR_API_KEY")

HEADERS = {
    "X-Api-Key": API_KEY,
    "Content-Type": "application/json"
}

def get_queue():
    """
    Retrieves the current download queue from Sonarr.
    """
    if not API_KEY:
        return {"error": "Sonarr API Key not configured"}

    url = f"{SERVER}/api/v3/queue"
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"error": str(e)}
