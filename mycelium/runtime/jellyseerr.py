import requests

JELLYSEERR_URL = "http://10.0.0.221:5055"
API_KEY = "MTc4MDYwNDkwOTc1M2M2OTBlYTdmLTY0OGMtNDNlNC1iOGIzLTkxZmZjZWNkYzYxNw=="


def request_media(title: str):
    url = f"{JELLYSEERR_URL}/api/v1/request"

    headers = {
        "X-Api-Key": API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "mediaType": "movie",
        "searchTitle": title
    }

    r = requests.post(url, json=payload, headers=headers)

    return {
        "status_code": r.status_code,
        "response": r.json() if r.text else {}
    }
