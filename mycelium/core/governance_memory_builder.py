from mycelium.core.governance_memory import store_memory


def build_memory_from_event(event):
    e = event["event"]
    data = event.get("data", {})

    tags = []

    # -------------------------
    # TAGGING RULES (semantic layer)
    # -------------------------

    if "mutation" in e:
        tags += ["mutation", "system_change"]

    if "rollback" in e:
        tags += ["rollback", "stability"]

    if "human" in e:
        tags += ["human_in_loop"]

    if "simulation" in e:
        tags += ["simulation"]

    if "validation" in e:
        tags += ["validation"]

    if "rejected" in e:
        tags += ["risk", "failure"]

    if "committed" in e:
        tags += ["commit", "state_change"]

    summary = f"{e} :: {str(data)[:80]}"

    return store_memory(event, summary, tags)
