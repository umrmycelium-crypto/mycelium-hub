from mycelium.gemini_executor import run_gemini_command


def developer_handler(payload, context):
    """
    Handles developer-focused intents using the Gemini CLI.
    """
    # The 'query' can be a direct question, a request for analysis, 
    # or a command to act on a specific file.
    query = payload.get("query") or payload.get("text") or "Analyze the current codebase."

    # We construct a slightly more structured prompt to get better results 
    # from the Gemini CLI for engineering tasks.
    prompt = f"As a senior software engineer, please perform the following task: {query}"

    result = run_gemini_command(prompt)

    if "Error" in result:
        return {
            "status": "ERROR",
            "action": "developer.assist",
            "message": result
        }

    return {
        "status": "OK",
        "action": "developer.assist",
        "result": result.strip()
    }
