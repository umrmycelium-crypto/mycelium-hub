from mycelium.core.event_bus import EVENT_BUS

def ingest_audio_event(text: str, source: str = "audio"):
    EVENT_BUS.emit("media.audio.transcribed", {
        "source": source,
        "text": text
    })


def ingest_video_event(frame_meta: dict):
    EVENT_BUS.emit("media.video.frame", frame_meta)
