from flask import Flask, jsonify, request, send_file
import requests
from mycelium.router import dispatch_intent

app = Flask(__name__)

SERVICES = {
    "jellyfin": "http://10.0.0.221:8096",
    "overseerr": "http://localhost:5055",
    "radarr": "http://localhost:7878",
    "sonarr": "http://localhost:8989",
    "ollama": "http://localhost:11434"
}

# Initialize the OS Kernel on boot
kernel.start()

# Ensure critical device overrides (Sovereign Presence) are active on boot
onboarding_manager.trigger_device_connection("LX77F6RP9W", {"model": "iPhone 16 Pro Max", "owner": "Miliana"})

@app.route("/")
def home():
    return jsonify({
        "system": "Mycelium OS Online",
        "kernel": "Active",
        "services": SERVICES
    })

@app.route("/wolf")
def wolf_portal():
    return send_file("mycelium/runtime/portal.html")

@app.route("/architect")
def architect_portal():
    return send_file("mycelium/runtime/parent_portal.html")

@app.route("/status")
def status():

    return jsonify({
        "system": "Mycelium OS Online",
        "kernel": "Active",
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
    
    # Publish presence event to the Nervous Bus
    # The Kernel will pick this up and decide if a proactive greeting is needed
    event = SystemEvent(
        type="user.presence",
        payload={"status": status},
        source="vision_sensor"
    )
    nervous_bus.publish(event)
    
    return jsonify({"status": "event_published"}), 200

@app.route("/ai/<prompt>")
def ai(prompt):
    # User-initiated request still goes through the Intent Engine
    result = intent_engine.process(prompt)
    
    status = result.get("status")
    
    if status == "SUCCESS":
        return jsonify({
            "type": "intent",
            "intent": result.get("intent"),
            "response": result.get("result"),
            "method": result.get("method")
        })
    
    if status == "REQUIRES_CONFIRMATION":
        return jsonify({
            "type": "confirmation",
            "intent": result.get("intent"),
            "payload": result.get("payload"),
            "response": result.get("message")
        })

    if status == "UNKNOWN_INTENT":
        try:
            from mycelium.core.models import get_llm_model
            r = requests.post(SERVICES["ollama"] + "/api/generate", json={
                "model": get_llm_model(),
                "prompt": prompt,
                "stream": False
            })
            return jsonify({
                "type": "conversation",
                "response": r.json().get("response")
            })
        except Exception as e:
            return jsonify({"type": "error", "response": f"Brain error: {str(e)}"}), 500

    return jsonify({
        "type": "error",
        "response": result.get("message", "I encountered an error processing that request."),
        "details": result
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7000)
