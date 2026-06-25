import json
import pprint


def render(result: dict) -> str:
    """
    Human-friendly MSHELL output renderer.
    """

    if not isinstance(result, dict):
        return pprint.pformat(result)

    # structured intent responses
    if "status" in result:
        return json.dumps(result, indent=2, ensure_ascii=False)

    return pprint.pformat(result)
