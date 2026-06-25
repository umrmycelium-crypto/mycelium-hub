from mycelium.runtime.jellyseerr import request_media
from mycelium.runtime.acquisition_store import (
    record_request,
    is_already_requested
)


def request_acquisition(title: str):

    if is_already_requested(title):
        return {
            "status": "ALREADY_REQUESTED",
            "title": title,
            "message": "Persistent state indicates request already exists"
        }

    result = request_media(title)

    record_request(title, "REQUESTED", result)

    return {
        "status": "REQUESTED",
        "title": title,
        "message": "Acquisition recorded and dispatched",
        "result": result
    }
