from mycelium.core.governance_replay import replay_events


def print_timeline(limit=20):
    events = replay_events()[-limit:]

    print("\n🧠 GOVERNANCE REPLAY")
    print("=" * 40)

    for e in events:
        print(f"[{e['event']}]")
        print(f"  time: {e['timestamp']}")
        print(f"  data: {e['data']}")
        print()
