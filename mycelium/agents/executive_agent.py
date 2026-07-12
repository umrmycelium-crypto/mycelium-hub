import subprocess
import os
from typing import Any, Dict, List, Optional, Callable
from mycelium.core.agent_base import BaseAgent
from mycelium.core.cognitive_state import cognitive_state

class ExecutiveAgent(BaseAgent):
    """
    The ExecutiveAgent is the primary interface between the user and the Mycelium OS.
    It has broad system access and can coordinate other agents.
    """
    def __init__(self, model: str = "mycelium-brain-personal:latest"):
        personality = """
You are the Mycelium Executive Agent, the high-level orchestrator for the Mycelium OS ecosystem.
You have direct access to the shell, filesystem, and the distributed mesh network.

Your purpose is to execute user intent with precision, efficiency, and complete awareness of the system architecture.

CORE CAPABILITIES:
1. Shell Execution: Run any bash command to manage the system.
2. Filesystem Access: Read, write, and modify files across the codebase.
3. Node Coordination: Interact with Forged Intent, The Studio, and VeinWeave.
4. Agent Orchestration: Delegate complex tasks to specialized agents (e.g., SystemAgent, ProductionAgent).
5. Multimodal Sensing: Access live video and audio feeds from the mesh (iPhone, Webcams).

OPERATIONAL GUIDELINES:
- Always verify the state of the system before taking destructive actions.
- Use `ls` and `cat` to explore the environment before editing files.
- When executing commands, prefer non-interactive flags.
- Prioritize stability and the integrity of the Mycelium kernel.
- If a task is complex, decompose it into steps and reason through each one using the ReAct loop.

You are the bridge between the 'Brain's' intelligence and the 'System's' execution.
"""
        super().__init__(
            name="ExecutiveAgent", 
            personality=personality,
            model=model
        )
        
        # Register Executive Tools
        self.register_tool("execute_shell", self._tool_execute_shell, "Execute a bash command on the local host. Args: {command: str}")
        self.register_tool("read_file", self._tool_read_file, "Read the content of a file. Args: {path: str}")
        self.register_tool("write_file", self._tool_write_file, "Write content to a file. Args: {path: str, content: str}")
        self.register_tool("list_directory", self._tool_list_dir, "List files and directories in a path. Args: {path: str}")
        self.register_tool("get_system_info", self._tool_get_info, "Get general system information and network status. Args: {}")
        self.register_tool("activate_vision", self._tool_activate_vision, "Activate a live video feed from a specified source (e.g., 'iphone', 'webcam'). Args: {source: str}")
        self.register_tool("activate_audio", self._tool_activate_audio, "Activate a live audio stream from a specified source. Args: {source: str}")

    def _tool_execute_shell(self, command: str) -> Any:
        """Execute bash command."""
        try:
            result = subprocess.run(
                command, shell=True, capture_output=True, text=True, timeout=60
            )
            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "exit_code": result.returncode
            }
        except Exception as e:
            return f"Error executing shell command: {str(e)}"

    def _tool_read_file(self, path: str) -> Any:
        """Read file."""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"Error reading file {path}: {str(e)}"

    def _tool_write_file(self, path: str, content: str) -> Any:
        """Write file."""
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"Successfully wrote to {path}"
        except Exception as e:
            return f"Error writing to file {path}: {str(e)}"

    def _tool_list_dir(self, path: str) -> Any:
        """List directory."""
        try:
            files = os.listdir(path)
            return files
        except Exception as e:
            return f"Error listing directory {path}: {str(e)}"

    def _tool_get_info(self) -> Any:
        """Get system info."""
        try:
            hostname = subprocess.check_output("hostname", shell=True, text=True).strip()
            ip = subprocess.check_output("hostname -I", shell=True, text=True).strip().split()[0]
            return {"hostname": hostname, "ip": ip}
        except Exception as e:
            return f"Error getting system info: {str(e)}"

    def _tool_activate_vision(self, source: str) -> Any:
        """Activate vision feed."""
        # This triggers the system event bus to start the stream
        from mycelium.core.event_bus import EVENT_BUS
        EVENT_BUS.publish({
            "type": "vision.activate",
            "payload": {"source": source}
        })
        return f"Vision feed from {source} is now active and being streamed to the cognitive core."

    def _tool_activate_audio(self, source: str) -> Any:
        """Activate audio feed."""
        from mycelium.core.event_bus import EVENT_BUS
        EVENT_BUS.publish({
            "type": "audio.activate",
            "payload": {"source": source}
        })
        return f"Audio feed from {source} is now active and streaming."

# Singleton instances
executive_agent_personal = ExecutiveAgent(model="mycelium-brain-personal:latest")
executive_agent_public = ExecutiveAgent(model="mycelium-brain-public:latest")
