import os
import glob
from typing import List, Dict, Any

class KnowledgeTool:
    """
    Provides the Executive Agent with a set of capabilities to interact 
    with the Obsidian knowledge vault.
    """
    def __init__(self, vault_path: str = "/home/mycelium/mycelium-hub"):
        self.vault_path = vault_path

    def search_notes(self, query: str) -> List[Dict[str, Any]]:
        """
        Searches for markdown files containing the query string.
        """
        results = []
        # Search recursively for .md files
        search_pattern = os.path.join(self.vault_path, "**/*.md")
        for file_path in glob.glob(search_pattern, recursive=True):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if query.lower() in content.lower():
                        results.append({
                            "path": file_path,
                            "name": os.path.basename(file_path),
                            "snippet": content[:200] + "..."
                        })
            except Exception as e:
                continue
        return results

    def read_note(self, path: str) -> str:
        """
        Reads the full content of a specific note.
        """
        try:
            # Security check: ensure path is within vault
            if not os.path.abspath(path).startswith(os.path.abspath(self.vault_path)):
                return "Error: Attempted to read file outside of the knowledge vault."
                
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"Error reading note: {str(e)}"

    def create_note(self, title: str, content: str) -> str:
        """
        Creates a new markdown note in the vault.
        """
        try:
            file_path = os.path.join(self.vault_path, f"{title}.md")
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"Successfully created note: {title}.md"
        except Exception as e:
            return f"Error creating note: {str(e)}"

    def append_to_note(self, path: str, text: str) -> str:
        """
        Appends text to an existing note. Useful for logging insights.
        """
        try:
            if not os.path.abspath(path).startswith(os.path.abspath(self.vault_path)):
                return "Error: Attempted to modify file outside of the knowledge vault."
                
            with open(path, 'a', encoding='utf-8') as f:
                f.write(f"

{text}")
            return f"Successfully appended to {os.path.basename(path)}"
        except Exception as e:
            return f"Error appending to note: {str(e)}"
