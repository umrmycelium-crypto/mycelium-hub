from mycelium.core.patch_executor import apply_patch


def system_apply_patch(payload, context):
    patch = payload.get("patch", "")

    return apply_patch(patch)
