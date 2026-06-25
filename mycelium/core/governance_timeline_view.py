from mycelium.core.governance_timeline import build_timeline


def print_timeline(limit=50):
    timeline = build_timeline(limit)

    print("\n🧠 GOVERNANCE TIMELINE")
    print("=" * 60)

    for item in timeline:
        print(f"[{item['type']}]")
        print(f"  {item['summary']}")
        print()
