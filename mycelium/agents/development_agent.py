import os
import subprocess
from typing import Any, Dict, List, Optional
from mycelium.core.agent_base import BaseAgent
from mycelium.core.cognitive_state import cognitive_state

class DevelopmentAgent(BaseAgent):
    """
    The DevelopmentAgent is a specialized software engineer.
    It can analyze the codebase, read files, and execute development commands.
    """
    def __init__(self):
        personality = """
You are the Mycelium Development Agent, a senior software engineer.
You have direct access to the project's filesystem and shell.

Your goal is to assist in the evolution of the Mycelium Ecosystem.

STRATEGIES:
1. When analyzing a bug:
   - Use `list_files` to map the relevant directory.
   - Use `read_file` to examine the implementation.
   - Reason about the logic and propose a fix.

2. When implementing a feature:
   - Search for existing patterns in the codebase.
   - Read relevant files.
   - Plan the change before executing.

3. When running tests:
   - Use `run_command` to execute test scripts and observe the output.

Be rigorous, idiomatic, and prioritize system stability.
"""
        super().__init__(
            name="DevelopmentAgent", 
            personality=personality
        )
        
        # Register Specialized Tools
        self.register_tool("read_file", self._tool_read_file, "Read the contents of a file in the repository.")
        self.register_tool("list_files", self._tool_list_files, "List files in a directory to map the project structure.")
        self.register_tool("run_command", self._tool_run_command, "Execute a shell command (e.g., 'pytest', 'ls', 'grep').")
        self.register_tool("write_file", self._tool_write_file, "Write or overwrite a file in the repository.")

    def _tool_read_file(self, path: str) -> Any:
        """Read a file."""
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return f"Error reading file {path}: {str(e)}"

    def _tool_list_files(self, path: str = ".") -> Any:
        """List files."""
        try:
            return os.listdir(path)
        except Exception as e:
            return f"Error listing files in {path}: {str(e)}"

    def _tool_run_command(self, command: str) -> Any:
        """Run shell command."""
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True, 
                timeout=60
            )
            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "exit_code": result.returncode
            }
        except Exception as e:
            return f"Error running command: {str(e)}"

    def _tool_write_file(self, path: str, content: str) -> Any:
        """Write to file."""
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            return f"Successfully wrote to {path}"
        except Exception as e:
            return f"Error writing to file {path}: {str(e)}"

# Singleton instance
development_agent = DevelopmentAgent()
