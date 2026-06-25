"""
Mycelium token counter.

Uses tiktoken (cl100k_base) for accurate token estimation across
OpenAI/Gemini/Ollama model families. All compilers and executors
MUST go through this module to enforce budget guarantees.
"""
import tiktoken

# cl100k_base is the closest universal approximation; matches
# GPT-4, GPT-3.5-turbo, and is within ~5% of Gemini and Llama 3
# tokenizers for English/code/JSON content.
_ENCODING = tiktoken.get_encoding("cl100k_base")


def estimate_tokens(text: str) -> int:
    """Accurate token count for a string. Empty string -> 0."""
    if not text:
        return 0
    return len(_ENCODING.encode(text, disallowed_special=()))


def estimate_messages(messages: list) -> int:
    """Token estimate for a list of chat messages (OpenAI format).

    Includes the per-message overhead (~4 tokens) that models charge.
    """
    if not messages:
        return 0
    total = 0
    for msg in messages:
        # Per-message structural overhead
        total += 4
        for value in msg.values():
            if isinstance(value, str):
                total += estimate_tokens(value)
    # Conversation-level overhead
    total += 2
    return total
