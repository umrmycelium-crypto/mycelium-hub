def format_result(result: dict) -> str:
    """
    Human-readable CLI output layer
    """

    if not isinstance(result, dict):
        return str(result)

    lines = ["\n📦 RESULT\n"]

    for k, v in result.items():
        lines.append(f"{k}: {v}")

    return "\n".join(lines)
