from mycelium.core.governance_timeline import build_timeline


def export_html(path="timeline.html", limit=200):
    timeline = build_timeline(limit)

    html = """
    <html>
    <head>
        <title>Governance Timeline</title>
        <style>
            body { font-family: monospace; background: #111; color: #0f0; }
            .event { margin-bottom: 12px; }
            .type { color: #ffcc00; }
        </style>
    </head>
    <body>
        <h2>Governance Timeline</h2>
    """

    for e in timeline:
        html += f"""
        <div class="event">
            <div class="type">{e['type']}</div>
            <div>{e['summary']}</div>
        </div>
        """

    html += "</body></html>"

    with open(path, "w") as f:
        f.write(html)

    return {"status": "exported", "path": path}
