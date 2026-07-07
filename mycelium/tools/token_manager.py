import secrets
import json
import os
from datetime import datetime, timedelta

TOKEN_FILE = "guest_tokens.json"

def generate_token(label="Guest", days_valid=365):
    """Generates a secure random token and saves it to the store."""
    token = secrets.token_urlsafe(16)
    expiry = (datetime.now() + timedelta(days=days_valid)).isoformat()
    
    data = {}
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'r') as f:
            data = json.load(f)
            
    data[token] = {
        "label": label,
        "created_at": datetime.now().isoformat(),
        "expiry": expiry,
        "permissions": ["read_metrics", "view_field"]
    }
    
    with open(TOKEN_FILE, 'w') as f:
        json.dump(data, f, indent=4)
        
    return token

if __name__ == "__main__":
    import sys
    label = sys.argv[1] if len(sys.argv) > 1 else "Guest"
    new_token = generate_token(label)
    print(f"✅ Generated {label} token: {new_token}")
    print(f"🔗 Access URL: http://mycelium.world/guest/{new_token}")
