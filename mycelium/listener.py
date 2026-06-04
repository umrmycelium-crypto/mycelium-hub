import whisper
import sounddevice as sd
import scipy.io.wavfile as wav
import os
from .router import detect_intent
from .actions import execute

def listen_and_route():
    # Load model (using 'base' for speed, consider 'small' for better accuracy)
    model = whisper.load_model("base")
    RATE = 16000
    DURATION = 5  # seconds

    print(f"Listening for {DURATION} seconds...")
    recording = sd.rec(
        int(DURATION * RATE),
        samplerate=RATE,
        channels=1,
        dtype="int16"
    )
    sd.wait()
    
    temp_file = "temp_voice.wav"
    wav.write(temp_file, RATE, recording)

    print("Transcribing...")
    result = model.transcribe(temp_file)
    text = result["text"].strip()
    
    # Cleanup temp file
    if os.path.exists(temp_file):
        os.remove(temp_file)

    if not text:
        print("No speech detected.")
        return

    print(f"TEXT: {text}")
    intent = detect_intent(text)
    print(f"INTENT: {intent}")
    
    result = execute(intent, text)
    print(f"[{result['status'].upper()}] {result['message']}")

if __name__ == "__main__":
    listen_and_route()
