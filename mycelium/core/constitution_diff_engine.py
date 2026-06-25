import copy


def diff_constitutions(old, new):
    """
    Field-level diff between constitution versions.
    """

    added = {}
    removed = {}
    changed = {}

    all_keys = set(old.keys()) | set(new.keys())

    for k in all_keys:
        if k not in old:
            added[k] = new[k]
        elif k not in new:
            removed[k] = old[k]
        elif old[k] != new[k]:
            changed[k] = {
                "from": old[k],
                "to": new[k]
            }

    return {
        "added": added,
        "removed": removed,
        "changed": changed
    }
