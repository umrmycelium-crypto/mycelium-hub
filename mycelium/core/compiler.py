import json
from mycelium.core.compiler_memory import COMPILER_MEMORY


class IntentCompiler:

    @staticmethod
    def compile(input_str: str):
        """
        Converts raw MSHELL input → normalized intent dict
        """

        # -------------------------
        # JSON INTENT MODE
        # -------------------------
        try:
            data = json.loads(input_str)

            return {
                "name": data.get("intent") or data.get("name"),
                "payload": data.get("payload", {}),
                "context": data.get("context", {})
            }

        except Exception:
            pass

        input_str = input_str.strip()

        # -------------------------
        # SYSTEM COMMANDS
        # -------------------------
        if input_str.startswith("system."):
            return {
                "name": input_str,
                "payload": {},
                "context": {"source": "mshell"}
            }

        # -------------------------
        # MEDIA COMMANDS
        # -------------------------
        if input_str.startswith("play "):
            return {
                "name": "media.play",
                "payload": {
                    "title": input_str.replace("play ", "", 1).strip()
                },
                "context": {"source": "mshell"}
            }

        # -------------------------
        # AI COMMANDS
        # -------------------------
        if input_str.startswith("ask "):
            return {
                "name": "ai.ask",
                "payload": {
                    "prompt": input_str.replace("ask ", "", 1).strip()
                },
                "context": {"source": "mshell"}
            }

        # -------------------------
        # EXPLAIN COMMANDS
        # -------------------------
        if input_str.startswith("explain "):
            return {
                "name": "system.auto.explain",
                "payload": {
                    "raw": input_str.replace("explain ", "", 1).strip()
                },
                "context": {"source": "mshell"}
            }

        # -------------------------
        # REPAIR COMMANDS
        # -------------------------
        if input_str.startswith("repair "):
            return {
                "name": "system.repair.analyze",
                "payload": {
                    "query": input_str.replace("repair ", "", 1).strip()
                },
                "context": {"source": "mshell"}
            }

        # -------------------------
        # FALLBACK (MISS LOGGING)
        # -------------------------
        COMPILER_MEMORY.record_miss(input_str)

        return {
            "name": "system.unknown",
            "payload": {
                "raw": input_str
            },
            "context": {
                "source": "mshell",
                "learnable": True
            }
        }
