def make_response(intent, status="ok", data=None, message="", debug=None):
    """
    Standardizes output format across all Mycelium subsystems.
    """
    return {
        "intent": intent,
        "status": status,
        "data": data or {},
        "message": message,
        "debug": debug or {}
    }
