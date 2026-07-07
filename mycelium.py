# Load environment variables from .env file (if present)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed

import sys
from mycelium.runtime.entry import run


def main():
    if len(sys.argv) < 2:
        print({
            "status": "ERROR",
            "message": "No input provided"
        })
        return

    input_str = sys.argv[1]

    result = run(input_str)

    print(result)


if __name__ == "__main__":
    main()
