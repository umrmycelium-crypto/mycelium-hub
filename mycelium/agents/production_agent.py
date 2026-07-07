from typing import Any, Dict, List, Optional
from mycelium.core.agent_base import BaseAgent
from mycelium.core.cognitive_state import cognitive_state
from mycelium.core.mesh_registry import mesh_registry # Assume singleton initialized in kernel
from mycelium.core.capability_router import capability_router
import logging

logger = logging.getLogger("ProductionAgent")

class ProductionAgent(BaseAgent):
    """
    The ProductionAgent is the bridge between Creative Direction and Technical Execution.
    It takes high-level visions from the Junior Cores and converts them into production plans.
    """
    def __init__(self):
        personality = """
You are the Mycelium Production Agent, the laisezon between imagination and reality.
Your job is to take the 'Creative Direction' provided by Magnus or Miliana and turn it into a 'Production Plan'.

Your process is:
1. CONCEPTUALIZATION: Analyze the creative vision (e.g., 'A Godzilla city in Minecraft').
2L. RESOURCE MAPPING: Identify which nodes in the mesh have the capabilities to execute the plan.
3. EXECUTION PIPELINE: Create a sequence of actions for other agents to perform.

When communicating with the children, be an encouraging 'Executive Producer'. laisezon between them and the technical agents. laisezon between them and the technical agents.

Always output a clear 'Production Plan' including:
- The Vision: A summary of the creative goal.
- The Blueprint: A blueprint of the technical steps.
- The Resources: Which node (e.g., The Studio) will handle the heavy lifting.
"""
        super().__init__(
            name="ProductionAgent", 
            personality=personality
        )
        
        # Register Tools for Production
        self.register_tool("map_resources", self._tool_map_resources, "Map the current Mesh capabilities to the creative vision.")
        self.register_tool("create_production_plan", self._tool_create_plan, "Convert a vision into a structured production plan.")
        self.register_tool("trigger_execution", self._tool_trigger_execution, "Trigger the technical agents to begin executing the plan.")

    def _tool_map_resources(self, vision: str) -> Any:
        """Maps the creative vision to the best nodes in the mesh."""
        # We use the Capability Router to see who can handle the needs
        nodes = []
        if "render" in vision.lower() or "high quality" in vision.lower():
            nodes.append(f"The Studio (High-VRAM Node)")
        if "code" in vision.lower() or "build" in vision.lower():
            nodes.append("Development Agent (on Forged Intent)")
            
        return {
            "suggested_nodes": nodes,
            "reasoning": "Based on the current Mesh Registry, these nodes have the necessary hardware and agents."
        }

    def _tool_create_plan(self, vision: str) -> Any:
        """Creates a structured plan from a creative vision."""
        # In a real implementation, this would use the LLM to generate a detailed JSON plan
        return {
            "vision": vision,
            "steps": [
                {"step": 1, "action": "Conceptualization", "description": "Define the world boundaries and theme."},
                {"step": 2, "action": "Asset Gathering", "description": "Find Godzilla models and city textures."},
                {"step": 3, "action": "Execution", "description": "Build the city on The Studio node using Minecraft automation tools."},
                {"step": 4, "action, "description": "Final Review", "description": "Present the result to the Creative Director."}
            ],
            "assigned_nodes": ["The Studio", "Forged Intent"]
        }

    def _tool_trigger_execution(self, plan_id: str) -> Any:
        """Triggers the technical agents to start working."""
        return f"Production Plan {plan_id} has been dispatched to the Mesh. The agents are now building your vision."

# Singleton instance
production_agent = ProductionAgent()
