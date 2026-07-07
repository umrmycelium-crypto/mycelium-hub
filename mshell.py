# Load environment variables from .env file (if present)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed

from mycelium.core.bootstrap_kernel import bootstrap
from mycelium.core.router import route
from mycelium.core.compiler import IntentCompiler


def main():
    state = bootstrap()
    print("🧠 Mycelium Kernel Ready")
    print(state)

    while True:
        try:
            raw = input("mshell> ")
            intent = IntentCompiler.compile(raw)
            result = route(intent)
            print("\n📦 RESULT\n")
            print(result)

        except Exception as e:
            print("ERROR:", e)


if __name__ == "__main__":
    main()
