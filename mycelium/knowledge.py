import os
import glob

# Vault path established in convention
VAULT_PATH = os.path.expanduser("~/mycelium-vault")

def search_notes(query):
    """
    Scans the Obsidian vault for markdown files containing the query string.
    """
    results = []
    
    if not os.path.exists(VAULT_PATH):
        return {"error": f"Vault path not found: {VAULT_PATH}"}

    # Search recursively for .md files
    search_pattern = os.path.join(VAULT_PATH, "**/*.md")
    for file_path in glob.glob(search_pattern, recursive=True):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read().lower()
                if query.lower() in content:
                    # Return relative path for cleaner output
                    rel_path = os.path.relpath(file_path, VAULT_PATH)
                    results.append(rel_path)
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            
    return results
