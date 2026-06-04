from .core.registry import register_all
from .core.replay import replay
import json

def main():
    print("🔁 Mycelium Event Replay Engine v0.1")
    print("-" * 40)
    
    # Initialize the current system state/bus
    bus = register_all()
    
    trace = replay(bus)
    
    if not trace:
        print("No events found in log to replay.")
        return

    for entry in trace:
        print(f"Replaying: {entry['event']}")
        print(f"Payload:   {entry['payload']}")
        
        for i, res in enumerate(entry['replayed_results']):
            status = res.get('status', 'unknown').upper()
            msg = res.get('message', '')
            print(f" Result {i+1}: [{status}] {msg}")
        print("-" * 20)

    print(f"\nReplay complete. Processed {len(trace)} event(s).")

if __name__ == "__main__":
    main()
