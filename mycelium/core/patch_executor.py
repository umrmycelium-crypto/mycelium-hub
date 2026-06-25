import subprocess
import json


def apply_patch(patch_text: str) -> dict:
    """
    Applies a unified diff patch safely using git apply.
    """

    try:
        proc = subprocess.run(
            ["git", "apply", "-"],
            input=patch_text.encode(),
            capture_output=True
        )

        if proc.returncode != 0:
            return {
                "status": "ERROR",
                "message": proc.stderr.decode()
            }

        return {
            "status": "APPLIED",
            "message": "patch applied successfully"
        }

    except Exception as e:
        return {
            "status": "ERROR",
            "message": str(e)
        }
