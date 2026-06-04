def normalize(result):
    """
    Normalize outputs so minor formatting differences don't trigger false diffs.
    Recursively sorts dictionaries and handles lists.
    """
    if result is None:
        return None

    if isinstance(result, list):
        return [normalize(r) for r in result]

    if isinstance(result, dict):
        # Sort keys to ensure deterministic comparison
        return {k: normalize(v) for k, v in sorted(result.items())}

    return result

def diff_events(original, replayed):
    """
    Compares original recorded results with replayed results.
    Returns a status and the normalized data for both.
    """
    orig = normalize(original)
    rep = normalize(replayed)

    if orig == rep:
        return {
            "status": "IDENTICAL",
            "original": orig,
            "replayed": rep
        }

    return {
        "status": "DRIFT_DETECTED",
        "original": orig,
        "replayed": rep
    }
