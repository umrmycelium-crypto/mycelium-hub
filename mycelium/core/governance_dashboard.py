from flask import Flask, jsonify
from mycelium.core.governance_events import get_events
from mycelium.core.governance_graph import build_graph

app = Flask(__name__)


@app.route("/events")
def events():
    return jsonify(get_events()[-200:])


@app.route("/graph")
def graph():
    return jsonify(build_graph())


@app.route("/")
def home():
    return """
    <html>
    <body>
        <h2>Mycelium Governance Dashboard</h2>
        <p>Endpoints:</p>
        <ul>
            <li>/events</li>
            <li>/graph</li>
        </ul>
    </body>
    </html>
    """


def run_dashboard():
    app.run(host="0.0.0.0", port=5005)

from flask import Response
import json
import time

from mycelium.core.governance_telemetry import subscribe

event_buffer = []


def stream_event(event):
    event_buffer.append(event)


subscribe("events", stream_event)


def stream():
    def generate():
        last_index = 0
        while True:
            if len(event_buffer) > last_index:
                new_events = event_buffer[last_index:]
                last_index = len(event_buffer)

                yield f"data: {json.dumps(new_events)}\n\n"

            time.sleep(0.5)

    return Response(generate(), mimetype="text/event-stream")


@app.route("/stream")
def stream_route():
    return stream()
