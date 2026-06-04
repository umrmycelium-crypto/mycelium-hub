from .router import detect_intent
from .core.registry import register_all
import json

def main():
    print("Mycelium Intent Engine v0.4 (Event Bus Mode - Type 'exit' to quit)")
    
    # Initialize Registry and Bus
    bus = register_all()
    
    while True:
        try:
            command = input("> ")
            if command.lower() in ["exit", "quit"]:
                break
                
            intent = detect_intent(command)
            
            # Publish event to the bus
            # Note: bus.publish returns a list of results from all subscribers
            results = bus.publish(intent, {"text": command})
            
            if not results:
                print(f"[UNKNOWN] No subscribers for intent: {intent}")
                continue

            # For v0.4, we primarily handle the first result (main action)
            result = results[0]
            
            # Print user-friendly message
            print(f"[{result['status'].upper()}] {result['message']}")
            
            # Special handling for developer analysis
            if result['intent'] == 'developer.assist' and result['status'] == 'ok':
                 print("\nAnalysis Output:")
                 print(result['data'].get('analysis'))
            elif result['data'] and result['intent'] not in ['media.play', 'media.search']:
                print(f"Data: {result['data']}")
            
        except EOFError:
            break
        except KeyboardInterrupt:
            print("\nExiting...")
            break

if __name__ == "__main__":
    main()
