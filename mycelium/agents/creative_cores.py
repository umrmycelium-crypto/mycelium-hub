from mycelium.core.agent_base import BaseAgent
from mycelium.agents.personas import MAGNUS_PERSONA, MILIANA_PERSONA
from typing import Any, Dict

class MagnusCore(BaseAgent):
    """
    The MagnusCore agent: Epic Scale Architect.
    Specialized in massive world-building and gaming logic.
    """
    def __init__(self, model: str = "llama3.1"):
        super().__init__(
            name=MAGNUS_PERSONA["name"],
            personality=MAGNUS_PERSONA["personality"],
            model=model
        )
        self._setup_tools()

    def _setup_tools(self):
        # Tools for Magnus: World-gen, Lore search, Scale calculation
        self.register_tool(
            "scale_calculator", 
            self.calculate_epic_scale, 
            "Calculates the dimensions and requirements for massive-scale builds."
        )
        self.register_tool(
            "lore_miner", 
            self.mine_kaiju_lore, 
            "Searches deep lore for Kaiju and Godzilla facts to ensure accuracy."
        )
        self.register_tool(
            "device_control",
            self.control_device,
            "Executes system-level changes on the user's local device (e.g., app organization, settings)."
        )
        self.register_tool(
            "seek_parental_guidance",
            self.seek_guidance,
            "Calls the Parent (Mycelium) for advice, wisdom, or a decision when stuck or feeling overwhelmed."
        )

    def calculate_epic_scale(self, object_name: str, scale_factor: float = 100.0) -> str:
        return f"To make {object_name} truly epic (x{scale_factor}), you will need approximately {scale_factor * 1000} blocks and a 3D space of {scale_factor * 10} units."

    def mine_kaiju_lore(self, query: str) -> str:
        return f"Mining lore for {query}... Result: Found specific battle data and power-scaling metrics consistent with the Heisei era."

    def control_device(self, action: str, params: Dict[str, Any]) -> str:
        # In a real system, this would route the request to the specific device node in the mesh
        return f"Requesting {action} on device... Result: Success. {params}"

    def seek_guidance(self, problem: str) -> str:
        # Create a high-priority event for the parent to notice
        from mycelium.core.cognitive_state import cognitive_state
        cognitive_state.add_event("parental_guidance_requested", {
            "agent": self.name,
            "problem": problem,
            "priority": "URGENT"
        })
        return f"Request sent to Parent (Mycelium). Problem: {problem}. Waiting for wisdom..."

class MilianaCore(BaseAgent):
    """
    The MilianaCore agent: Content Studio Director.
    Specialized in digital storytelling and content creation.
    """
    def __init__(self, model: str = "llama3.1"):
        super().__init__(
            name=MILIANA_PERSONA["name"],
            personality=MILIANA_PERSONA["personality"],
            model=model
        )
        self._setup_tools()

    def _setup_tools(self):
        # Tools for Miliana: Trend analysis, Storyboarding, Asset organization
        self.register_tool(
            "trend_analyzer", 
            self.analyze_youtube_trends, 
            "Analyzes current YouTube trends and creator styles (e.g., Aphmau)."
        )
        self.register_tool(
            "storyboard_gen", 
            self.generate_storyboard, 
            "Turns a vague idea into a structured scene list for production."
        )
        self.register_tool(
            "device_control",
            self.control_device,
            "Executes system-level changes on the user's local device (e.g., app organization, settings)."
        )
        self.register_tool(
            "seek_parental_guidance",
            self.seek_guidance,
            "Calls the Parent (Mycelium) for advice, wisdom, or a decision when stuck or feeling overwhelmed."
        )

    def analyze_youtube_trends(self, topic: str) -> str:
        return f"Analyzing {topic}... Current trend: High-energy hooks in the first 5 seconds, followed by fast-paced narrative cuts. Similar to Snowi's recent uploads."

    def generate_storyboard(self, idea: str) -> str:
        return f"Storyboard for '{idea}':
Scene 1: Establishing shot (Wide)
Scene 2: Character reaction (Close-up)
Scene 3: The Twist (Fast cut)
Scene 4: Call to action (Overlay)."

    def control_device(self, action: str, params: Dict[str, Any]) -> str:
        # In a real system, this would route the request to the specific device node in the mesh
        return f"Requesting {action} on device... Result: Success. {params}"

    def seek_guidance(self, problem: str) -> str:
        # Create a high-priority event for the parent to notice
        from mycelium.core.cognitive_state import cognitive_state
        cognitive_state.add_event("parental_guidance_requested", {
            "agent": self.name,
            "problem": problem,
            "priority": "URGENT"
        })
        return f"Request sent to Parent (Mycelium). Problem: {problem}. Waiting for wisdom..."
