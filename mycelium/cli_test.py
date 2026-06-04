from .router import detect_intent
from .actions import execute
import json

def main():
    print("Mycelium Intent Engine v0.3 (Normalized Output Mode - Type 'exit' to quit)")
    while True:
        try:
            command = input("> ")
            if command.lower() in ["exit", "quit"]:
                break
                
            intent = detect_intent(command)
            result = execute(intent, command)
            
            # Print user-friendly message
            print(f"[{result['status'].upper()}] {result['message']}")
            
            # Optionally print full data if significant
            if result['intent'] == 'developer.assist' and result['status'] == 'ok':
                 print("\nAnalysis Output:")
                 print(result['data'].get('analysis'))
            elif result['data'] and result['intent'] != 'media.play':
                print(f"Data: {result['data']}")
            
        except EOFError:
            break
        except KeyboardInterrupt:
            print("\nExiting...")
            break

if __name__ == "__main__":
    main()
