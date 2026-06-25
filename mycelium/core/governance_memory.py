from collections import defaultdict

MEMORY = []
TAG_INDEX = defaultdict(list)


def store_memory(event, summary, tags):
    entry = {
        "event": event,
        "summary": summary,
        "tags": tags
    }

    MEMORY.append(entry)

    for t in tags:
        TAG_INDEX[t].append(entry)

    return entry


def search_by_tag(tag):
    return TAG_INDEX.get(tag, [])


def get_all_memory():
    return MEMORY
