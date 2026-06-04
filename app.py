from flask import Flask, jsonify
import requests

app = Flask(__name__)

SERVICES = {
    "jellyfin": "http://10.0.0.221:8096",
    "overseerr": "http://localhost:5055",
    "radarr": "http://localhost:7878",
    "sonarr": "http://localhost:8989",
    "ollama": "http://localhost:11434"
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

@app.route("/ai/<prompt>")
def ai(prompt):
    r = requests.post(SERVICES["ollama"] + "/api/generate", json={
        "model": "llama3.1",
        "prompt": prompt,
        "stream": False
    })
    return jsonify(r.json())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7000)
