from mycelium.core.agent import MyceliumAgent


def format_output(result):
    """
    Clean CLI rendering layer (fixes your ugly JSON dumps)
    """

    if isinstance(result, dict):
        print("\n📦 RESULT\n")
        for k, v in result.items():
            print(f"{k}: {v}")
        print("")
    else:
        print(result)


def main():
    print("🧠 Mycelium Agent CLI v1 (type 'exit')")

    agent = MyceliumAgent()

    while True:
        try:
            raw = input("agent> ").strip()

            if raw == "exit":
                break

            result = agent.run(raw)
            format_output(result)

        except Exception as e:
            print({
                "status": "ERROR",
                "message": str(e)
            })


if __name__ == "__main__":
    main()
