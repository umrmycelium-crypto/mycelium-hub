def media_agent(signal, brain):

    if signal.type == "media.play":

        title = signal.payload.get("title")

        brain.append("last_actions", f"played {title}")

        return {
            "status": "OK",
            "action": "playing",
            "title": title
        }

    if signal.type == "media.search":
        return {
            "status": "OK",
            "results": []
        }
