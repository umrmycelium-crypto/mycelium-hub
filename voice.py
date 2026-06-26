import whisper
import sounddevice as sd
import scipy.io.wavfile as wav
import requests
import numpy as np
import time
import threading
import os
import subprocess
from flask import Flask, request, jsonify
from mycelium.core.speech_adaptor import SPEECH_ADAPTOR

# --- Configuration ---
MODEL_PATH = "models/en_US-lessac-medium.onnx"
CONFIG_PATH = "models/en_US-lessac-medium.onnx.json"
WHISPER_MODEL_TYPE = "base"
VOICE_SERVER_PORT = 7001

# --- TTS Controller (Handles Interruption) ---
class SpeechController:
    def __init__(self):
        self.current_process = None
        self.playback_thread = None
        self._stop_event = threading.Event()

    def stop(self):
        """Forcefully stop current speech."""
        if self.current_process:
            try:
                self.current_process.terminate()
                print("🛑 Interrupted AI speech.")
            except Exception:
                pass
            self.current_process = None
        self._stop_event.set()

    def speak(self, text):
        """Generate and play speech in a non-blocking way."""
        self.stop() 
        self._stop_event.clear()
        self.playback_thread = threading.Thread(target=self._run_tts, args=(text,))
        self.playback_thread.start()

    def _run_tts(self, text):
        try:
            print(f"🎙️ Generating speech for: {text}")
            cmd = ["piper", "--model", MODEL_PATH, "--config", CONFIG_PATH, "--output_file", "speech_output.wav"]
            process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate(input=text)
            if process.returncode != 0:
                print(f"❌ Piper Error: {stderr}")
                return

            print("🔊 Playing audio...")
            play_cmd = ["ffplay", "-nodisp", "-autoexit", "speech_output.wav"]
            # Capture stderr to see if ffplay has device issues
            self.current_process = subprocess.Popen(play_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
            
            # We don't want to block the thread entirely with .wait() if we want to be able to stop it, 
            # but the current logic uses .wait(). Let's keep it but capture the output on failure.
            stdout, stderr = self.current_process.communicate()
            if self.current_process.returncode != 0 and self.current_process.returncode != -15: # -15 is SIGTERM (expected on stop())
                print(f"❌ ffplay Error: {stderr}")
        except Exception as e:
            print(f"TTS Exception: {e}")

# Initialize Components
print("Loading Whisper model...")
whisper_model = whisper.load_model(WHISPER_MODEL_TYPE)
speech_ctrl = SpeechController()

# --- Voice Server for Proactive Speech ---
voice_app = Flask(__name__)

@voice_app.route("/speak", methods=["POST"])
def speak_endpoint():
    data = request.json
    text = data.get("text", "")
    if text:
        speech_ctrl.speak(text)
        return jsonify({"status": "speaking"}), 200
    return jsonify({"status": "no text"}), 400

def run_voice_server():
    voice_app.run(host="0.0.0.0", port=VOICE_SERVER_PORT, debug=False, use_reloader=False)

# --- Voice Sensing ---
def record_chunk(duration=4, fs=44100):
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    return fs, audio

def is_silent(audio, threshold=0.02):
    return np.max(np.abs(audio)) < threshold

def transcribe(fs, audio):
    wav.write("voice_temp.wav", fs, audio)
    # task="translate" ensures that any language detected is translated to English.
    # This also helps reduce some types of hallucinations.
    result = whisper_model.transcribe("voice_temp.wav", task="translate")
    return result["text"].strip()

def send_to_ai(text):
    if not text:
        return
    print(f"Sending to Mycelium: {text}")
    try:
        r = requests.get(f"http://localhost:7000/ai/{text}", timeout=60)
        response_data = r.json()
        if response_data.get("type") == "intent":
            msg = f"Intent {response_data.get('intent')} handled. {response_data.get('response')}"
            print(f"🎯 {msg}")
            speech_ctrl.speak(msg)
        else:
            response_text = response_data.get("response", "I'm not sure how to respond.")
            print(f"💬 AI: {response_text}")
            speech_ctrl.speak(response_text)
    except Exception as e:
        print(f"Error communicating with AI: {e}")

def main():
    # Start voice server in background
    server_thread = threading.Thread(target=run_voice_server, daemon=True)
    server_thread.start()
    
    print(f"Mycelium Voice Sensing Active on port {VOICE_SERVER_PORT}. (Ctrl+C to stop)")
    print("Barge-in enabled: Just speak to interrupt the AI.")
    
    try:
        while True:
            fs, audio = record_chunk()
            if not is_silent(audio):
                if speech_ctrl.current_process:
                    speech_ctrl.stop()
                text = transcribe(fs, audio)
                if text:
                    corrected_text = SPEECH_ADAPTOR.correct(text)
                    if corrected_text != text:
                        print(f"Adapted: {text} -> {corrected_text}")
                    print(f"You said: {corrected_text}")
                    send_to_ai(corrected_text)
                else:
                    print("... (noise detected)")
            else:
                time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nStopping voice sensing...")

if __name__ == "__main__":
    main()
