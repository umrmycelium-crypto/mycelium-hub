def validate_patch(patch: str):
    """
    Minimal safety filter before any registry change.
    """

    forbidden = [
        "os.system",
        "rm -rf",
        "subprocess",
        "eval",
        "exec"
    ]

    for f in forbidden:
        if f in patch:
            return {
                "approved": False,
                "reason": f"forbidden pattern detected: {f}"
            }

    return {
        "approved": True,
        "reason": "safe"
    }
