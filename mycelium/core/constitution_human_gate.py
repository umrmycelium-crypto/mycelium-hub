from mycelium.core.constitution_human_override import get_request


def require_human_approval(request_id):
    """
    Blocks execution unless explicitly approved by human.
    """

    request = get_request(request_id)

    if not request:
        return False, "missing_human_request"

    if request["status"] != "approve":
        return False, "not_approved_by_human"

    return True, "human_approved"
