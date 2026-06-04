from .router import detect_intent
from .core.registry import register_all
import json

def main():
    print("Mycelium Intent Engine v0.5 (Hybrid LLM Router - Type 'exit' to quit)")
    
    # Initialize Registry and Bus
    bus = register_all()
    
    while True:
        try:
            command = input("> ")
            if not command.strip():
                continue
            if command.lower() in ["exit", "quit"]:
                break
                
            # detect_intent now returns a dict with 'intent', 'confidence', 'entities'
            intent_data = detect_intent(command)
            intent = intent_data["intent"]
            
            # Use extracted entities as the primary payload
            payload = intent_data.get("entities", {})
            payload["text"] = command # Always include original text for fallback
            
            # Debug info (before execution)
            print(f"DEBUG: Detected Intent: {intent} (Confidence: {intent_data.get('confidence', 0):.2f})")
            if intent_data.get('entities'):
                print(f"DEBUG: Entities: {intent_data['entities']}")

            # Publish event to the bus
            results = bus.publish(intent, payload)
            
            if not results:
                print(f"[UNKNOWN] No subscribers for intent: {intent}")
                continue

            # For v0.5, we primarily handle the first result (main action)
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
