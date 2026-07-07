import json
import requests
import os
from typing import Any, Dict, List, Optional, Callable
from datetime import datetime
from mycelium.core.cognitive_state import cognitive_state
from mycelium.core.models import get_llm_model, OLLAMA_URL

class BaseAgent:
    """
    Base class for all Mycelium autonomous agents.
    Implements a ReAct (Reasoning + Acting) loop.
    """
    def __init__(self, name: str, personality: str, model: str = None):
        self.name = name
        self.personality = personality
        self.model = model or get_llm_model()
        self.tools = {}
        self.max_iterations = 15

    def register_tool(self, name: str, func: Callable, description: str):
        """
        Registers a tool that the agent can use.
        The description is passed to the LLM to help it decide when to use the tool.
        """
        self.tools[name] = {
            "func": func,
            "description": description
        }

    def _get_tool_descriptions(self) -> str:
        """Returns a formatted string of all available tools for the LLM."""
        descriptions = []
        for name, tool in self.tools.items():
            descriptions.append(f"- {name}: {tool['description']}")
        return "\n".join(descriptions)

    def _call_tool(self, tool_name: str, args: Dict[str, Any]) -> Any:
        """Executes a registered tool."""
        if tool_name not in self.tools:
            return f"Error: Tool {tool_name} not found."
        
        try:
            # Execute the tool and log it to working memory
            cognitive_state.add_event(f"{self.name}_used_tool", {"tool": tool_name, "args": args})
            return self.tools[tool_name]["func"](**args)
        except Exception as e:
            return f"Error executing tool {tool_name}: {str(e)}"

    def run(self, task_input: str) -> str:
        """
        The main ReAct loop.
        Think -> Act -> Observe -> Repeat.
        """
        # Start with the initial prompt
        history = []
        current_input = task_input
        
        # Prime the LLM with personality, tools, and cognitive state
        system_prompt = f"""
{self.personality}

AVAILABLE TOOLS:
{self._get_tool_descriptions()}

COGNITIVE STATE:
{cognitive_state.get_snapshot()}

You must operate in a loop:
1. THOUGHT: Reason about the current state and what tool to use.
2. ACTION: Specify a tool to call. Format: {{"action": "tool_name", "action_input": {{"arg1": "val1"}}}}
3. OBSERVATION: The result of the tool call.

If you have the final answer, respond with:
{{"final_answer": "Your final response to the user"}}

Rules:
- Output ONLY valid JSON.
- Do not include any text outside the JSON.
- If a tool call fails, reason about why and try a different approach.
"""
        
        iteration = 0
        while iteration < self.max_iterations:
            # Construct the prompt for this turn
            prompt = (
                f"{system_prompt}\n\n"
                f"User Input: {current_input}\n\n"
                f"Conversation History:\n{json.dumps(history)}"
            )
            
            try:
                response = requests.post(
                    OLLAMA_URL,
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False,
                        "format": "json"
                    },
                    timeout=30
                )
                
                res_data = response.json().get("response", "{}")
                res_json = json.loads(res_data)
                
                if "final_answer" in res_json:
                    return res_json["final_answer"]
                
                if "action" in res_json:
                    tool_name = res_json["action"]
                    tool_args = res_json.get("action_input", {})
                    
                    # Log the thought process
                    thought = res_json.get("thought", "No explicit thought provided.")
                    cognitive_state.add_event(f"{self.name}_thought", {"thought": thought})
                    
                    # Execute the tool
                    observation = self._call_tool(tool_name, tool_args)
                    
                    # Update history for the next turn
                    history.append({
                        "thought": thought,
                        "action": tool_name,
                        "action_input": tool_args,
                        "observation": observation
                    })
                    
                else:
                    # Fallback for unexpected LLM output
                    return "I'm sorry, I encountered an error in my reasoning process."
                    
            except Exception as e:
                return f"Agent Error: {str(e)}"
            
            iteration += 1
            
        return "I'm sorry, I was unable to complete the task within the maximum number of steps."

# This is a base class; a specific agent will inherit from it.
