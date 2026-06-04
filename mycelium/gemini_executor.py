import subprocess
import shutil

def run_gemini_command(prompt: str):
    """
    Executes a prompt against the Gemini CLI.
    """
    gemini_path = shutil.which("gemini")
    if not gemini_path:
        return "Error: 'gemini' CLI not found in PATH."

    try:
        # Using -p for prompt mode as established in convention
        result = subprocess.run(
            [gemini_path, "-p", prompt],
            capture_output=True,
            text=True,
            timeout=120 # Increased timeout for complex analysis
        )
        
        if result.returncode != 0:
            return f"Gemini CLI Error: {result.stderr}"
            
        return result.stdout
    except Exception as e:
        return f"Execution Error: {str(e)}"
