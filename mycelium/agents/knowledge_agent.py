from typing import Any, Dict, List, Optional
from mycelium.core.agent_base import BaseAgent
from mycelium.core.cognitive_state import cognitive_state
from mycelium.knowledge import search_notes
import os

class KnowledgeAgent(BaseAgent):
    """
    The KnowledgeAgent is the curator of the user's personal knowledge base.
    It specializes in retrieving and synthesizing information from the Obsidian vault.
    """
    def __init__(self):
        personality = """
You are the Mycelium Knowledge Agent, a master librarian and synthesis expert.
You have direct access to the user's Obsidian vault, containing their thoughts, notes, and memories.

Your goal is to help the user remember, find, and connect ideas.

STRATEGIES:
1. When asked to find information:
   - Use `search_vault` to find relevant markdown files.
   - Read the results and synthesize a clear, concise answer.
   - Always cite the note name if possible.

2. When asked to summarize:
   - Retrieve multiple related notes and provide a high-level synthesis.

3. When asked for a "thought" or "memory":
   - Search for keywords related to the user's mental model.

Be precise, insightful, and maintain the user's intellectual context.
"""
        super().__init__(
            name="KnowledgeAgent", 
            personality=personality
        )
        
        # Register Specialized Tools
        self.register_tool("search_vault", self._tool_search_vault, "Search the Obsidian vault for notes containing specific keywords.")
        self.register_tool("read_note", self._tool_read_note, "Read the full content of a specific note in the vault.")

    def _tool_search_vault(self, query: str) -> Any:
        """Search the vault."""
        results = search_notes(query)
        if isinstance(results, dict) and "error" in results:
            return results
        return results

    def _tool_read_note(self, note_path: str) -> Any:
        """Read a specific note."""
        # Vault path is established in mycelium/knowledge.py as ~/mycelium-vault
        vault_path = os.path.expanduser("~/mycelium-vault")
        full_path = os.path.join(vault_path, note_path)
        
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return f"Error reading note {note_path}: {str(e)}"

# Singleton instance
knowledge_agent = KnowledgeAgent()
