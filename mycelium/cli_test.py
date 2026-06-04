from .router import detect_intent
from .actions import execute

def main():
    print("Mycelium Intent Engine v0.2 (CLI Test Mode - Type 'exit' to quit)")
    while True:
        try:
            command = input("> ")
            if command.lower() in ["exit", "quit"]:
                break
                
            intent = detect_intent(command)
            print(f"Intent: {intent}")
            execute(intent, command)
            
        except EOFError:
            break
        except KeyboardInterrupt:
            print("\nExiting...")
            break

if __name__ == "__main__":
    main()
