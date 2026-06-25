import textwrap


def format_response(result: dict):
    """
    Clean MSHELL output layer
    """

    # AI RESPONSE
    if "response" in result:
        print("\n🧠 AI RESPONSE\n")
        print(textwrap.fill(result["response"], width=100))
        print()
        return

    # PATCH RESULT
    if result.get("status") == "PATCH_APPLIED":
        print("\n🩹 PATCH APPLIED\n")
        print("Path:", result["result"].get("path"))
        print("Status:", result["result"].get("status"))
        print()
        return

    # SYSTEM / DEFAULT
    print("\n📦 RESULT\n")
    for k, v in result.items():
        print(f"{k}: {v}")
    print()
