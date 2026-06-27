import requests
from urllib.parse import quote

JELLYSEERR_URL = "http://10.0.0.221:5055"
API_KEY = "MTc4MDYwNDkwOTc1M2M2OTBlYTdmLTY0OGMtNDNlNC1iOGIzLTkxZmZjZWNkYzYxNw=="


def request_media(title: str):
    # 1. Search for the media to get the ID
    search_url = f"{JELLYSEERR_URL}/api/v1/search"

    headers = {
        "X-Api-Key": API_KEY,
        "Content-Type": "application/json"
    }

    # Manually construct the query string to ensure encoding is handled correctly by the API
    encoded_title = quote(title)
    search_url_with_params = f"{search_url}?query={encoded_title}"
    search_r = requests.get(search_url_with_params, headers=headers)

    if search_r.status_code != 200:
        return {
            "status_code": search_r.status_code,
            "response": {"message": "Search failed", "error": search_r.text}
        }

    results = search_r.json().get("results", [])
    if not results:
        return {
            "status_code": 404,
            "response": {"message": f"No media found for title: {title}"}
        }

    # Use the first result
    best_match = results[0]
    media_id = best_match.get("id")
    media_type = best_match.get("mediaType", "movie")

    # 2. Request the media using the ID
    url = f"{JELLYSEERR_URL}/api/v1/request"

    payload = {
        "mediaType": media_type,
        "mediaId": media_id
    }

    r = requests.post(url, json=payload, headers=headers)

    return {
        "status_code": r.status_code,
        "response": r.json() if r.text else {}
    }
