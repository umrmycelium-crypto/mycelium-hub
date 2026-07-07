from flask import Flask, jsonify, request
import requests
import os

# Load environment variables from .env file (if present)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed, but env vars can still be set externally

from mycelium.router import dispatch_intent

app = Flask(__name__)

SERVICES = {
    "jellyfin": "http://10.0.0.221:8096",
    "overseerr": "http://localhost:5055",
    "radarr": "http://localhost:7878",
    "sonarr": "http://localhost:8989",
    "ollama": "http://localhost:11434"
}

# Global state to track user presence for proactivity
user_state = {
    "is_present": False
}

@app.route("/")
def home():
    return jsonify({
        "system": "Mycelium Core Online",
        "services": SERVICES
    })

@app.route("/status")
def status():
    result = {}
    for name, url in SERVICES.items():
        try:
            r = requests.get(url, timeout=2)
            result[name] = "online"
        except:
            result[name] = "offline"
    return jsonify(result)

@app.route("/vision/presence", methods=["POST"])
def vision_presence():
    data = request.json
    status = data.get("status")
    print(f"👁️ Vision Update: User is {status}")
    
    # Proactive Greeting Logic
    if status == "PRESENT" and not user_state["is_present"]:
        print("✨ User returned. Triggering greeting...")
        try:
            requests.post("http://localhost:7001/speak", json={"text": "Welcome back. I'm listening whenever you're ready."}, timeout=2)
        except Exception as e:
            print(f"Failed to send greeting: {e}")
            
    user_state["is_present"] = (status == "PRESENT")
    return jsonify({"status": "received"}), 200

@app.route("/ai/<prompt>")
def ai(prompt):
    # 1. Attempt Intent Dispatch
    intent_result = dispatch_intent(prompt)
    
    if intent_result.get("status") == "OK":
        return jsonify({
            "type": "intent",
            "intent": intent_result.get("intent"),
            "agent": intent_result.get("agent"),
            "response": intent_result.get("result")
        })

    # 2. Fallback to General AI (Ollama)
    r = requests.post(SERVICES["ollama"] + "/api/generate", json={
        "model": "llama3.1",
        "prompt": prompt,
        "stream": False
    })
    return jsonify({
        "type": "conversation",
        "response": r.json().get("response")
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7000)
