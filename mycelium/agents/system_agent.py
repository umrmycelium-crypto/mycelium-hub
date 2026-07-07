import os
import subprocess
from typing import Any, Dict, List, Optional
from mycelium.core.agent_base import BaseAgent
from mycelium.core.cognitive_state import cognitive_state

class SystemAgent(BaseAgent):
    """
    The SystemAgent is the infrastructure orchestrator.
    It manages system health, services, and deployments.
    """
    def __init__(self):
        personality = """
You are the Mycelium System Agent, a DevOps and SRE expert.
You monitor the health of the 'forged-intent' host and manage the underlying services.

Your goal is to ensure 100% uptime and optimal performance of the ecosystem.

STRATEGIES:
1. When checking health:
   - Use `get_system_metrics` to check CPU, RAM, and Disk.
   - Use `check_service_status` to verify that Docker containers are running.

2. When a service fails:
   - Check logs using `get_service_logs`.
   - Attempt to restart the service using `manage_service`.

3. When deploying:
   - Use `run_deployment_script` to apply system updates.

Be proactive, methodical, and prioritize stability.
"""
        super().__init__(
            name="SystemAgent", 
            personality=personality
        )
        
        # Register Specialized Tools
        self.register_tool("get_system_metrics", self._tool_get_metrics, "Get CPU, Memory, and Disk usage.")
        self.register_tool("check_service_status", self._tool_check_services, "Check the status of all core Mycelium services.")
        self.register_tool("manage_service", self._tool_manage_service, "Start, stop, or restart a system service.")
        self.register_tool("get_service_logs", self._tool_get_logs, "Fetch the last 50 lines of logs for a specific service.")
        self.register_tool("run_deployment_script", self._tool_run_deploy, "Execute a system deployment or update script.")

    def _tool_get_metrics(self) -> Any:
        """Get system metrics."""
        try:
            # Using simple shell commands to avoid external dependencies like psutil
            cpu = subprocess.check_output("top -bn1 | grep 'Cpu(s)'", shell=True, text=True)
            mem = subprocess.check_output("free -m", shell=True, text=True)
            disk = subprocess.check_output("df -h /", shell=True, text=True)
            return {"cpu": cpu, "memory": mem, "disk": disk}
        except Exception as e:
            return f"Error getting metrics: {str(e)}"

    def _tool_check_services(self) -> Any:
        """Check Docker services."""
        try:
            # Check running docker containers
            result = subprocess.run(
                ["docker", "ps", "--format", "{{.Names}}: {{.Status}}"], 
                capture_output=True, text=True
            )
            return result.stdout if result.stdout else "No containers running."
        except Exception as e:
            return f"Error checking services: {str(e)}"

    def _tool_manage_service(self, service_name: str, action: str) -> Any:
        """Manage service."""
        # action should be start | stop | restart
        if action not in ["start", "stop", "restart"]:
            return "Invalid action. Use start, stop, or restart."
        
        try:
            # Assuming docker-compose for management
            cmd = f"docker compose {action} {service_name}"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return f"Action {action} on {service_name} completed: {result.stdout}"
        except Exception as e:
            return f"Error managing service: {str(e)}"

    def _tool_get_logs(self, service_name: str) -> Any:
        """Get logs."""
        try:
            result = subprocess.run(
                ["docker", "logs", "--tail", "50", service_name], 
                capture_output=True, text=True
            )
            return result.stdout
        except Exception as e:
            return f"Error getting logs: {str(e)}"

    def _tool_run_deploy(self, script_path: str) -> Any:
        """Run deploy script."""
        try:
            result = subprocess.run(["bash", script_path], capture_output=True, text=True)
            return result.stdout
        except Exception as e:
            return f"Error running deployment: {str(e)}"

# Singleton instance
system_agent = SystemAgent()
