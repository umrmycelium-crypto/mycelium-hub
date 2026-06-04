import whisper
import sounddevice as sd
import scipy.io.wavfile as wav
import requests

model = whisper.load_model("base")

def record():
    fs = 44100
    duration = 4
    print("Listening...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    wav.write("voice.wav", fs, audio)

def transcribe():
    result = model.transcribe("voice.wav")
    return result["text"]

def send_to_ai(text):
    if not text:
        print("(no speech detected)")
        return
    r = requests.get(f"http://localhost:7000/ai/{text}", timeout=60)
    try:
        print(r.json())
    except requests.exceptions.JSONDecodeError:
        print(f"(non-JSON response: {r.status_code} {r.text[:120]})")

record()
text = transcribe()
print("You said:", text)
send_to_ai(text)
