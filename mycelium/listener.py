import whisper
import sounddevice as sd
import scipy.io.wavfile as wav
import os
from .router import detect_intent
from .core.registry import register_all

def listen_and_route():
    # Initialize Bus
    bus = register_all()
    
    # ... (keep existing model loading and recording logic)
    import whisper
    import sounddevice as sd
    import scipy.io.wavfile as wav
    import os

    model = whisper.load_model("base")
    RATE = 16000
    DURATION = 5

    print(f"Listening for {DURATION} seconds...")
    recording = sd.rec(int(DURATION * RATE), samplerate=RATE, channels=1, dtype="int16")
    sd.wait()
    
    temp_file = "temp_voice.wav"
    wav.write(temp_file, RATE, recording)

    print("Transcribing...")
    result = model.transcribe(temp_file)
    text = result["text"].strip()
    
    if os.path.exists(temp_file):
        os.remove(temp_file)

    if not text:
        print("No speech detected.")
        return

    print(f"TEXT: {text}")
    intent = detect_intent(text)
    print(f"INTENT: {intent}")
    
    # Publish to bus
    results = bus.publish(intent, {"text": text})
    if results:
        result = results[0]
        print(f"[{result['status'].upper()}] {result['message']}")

if __name__ == "__main__":
    listen_and_route()
