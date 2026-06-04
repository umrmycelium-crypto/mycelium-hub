from .core.registry import register_all
from .core.replay import replay
import json

def main():
    print("🔁 Mycelium Event Replay & Diff Engine v0.2")
    print("-" * 40)
    
    # Initialize the current system state/bus
    bus = register_all()
    
    trace = replay(bus)
    
    if not trace:
        print("No events found in log to replay.")
        return

    identical_count = 0
    drift_count = 0

    for entry in trace:
        event_name = entry['event']
        diff_status = entry['diff']['status']
        
        if diff_status == "IDENTICAL":
            print(f"✔ {event_name} → IDENTICAL")
            identical_count += 1
        else:
            print(f"⚠ {event_name} → DRIFT DETECTED")
            drift_count += 1
            print("  Original:", json.dumps(entry['diff']['original'], indent=2))
            print("  Replayed:", json.dumps(entry['diff']['replayed'], indent=2))
        
        print("-" * 20)

    print(f"\nReplay complete. Processed {len(trace)} event(s).")
    print(f"Identical: {identical_count}")
    print(f"Drift Detected: {drift_count}")

if __name__ == "__main__":
    main()
