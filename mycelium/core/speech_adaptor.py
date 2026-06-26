from collections import defaultdict
import json
import os

class SpeechAdaptor:
    """
    Learns user speech patterns and corrects recurring transcription errors.
    """
    def __init__(self, storage_path="state/speech_adaptor.json"):
        self.storage_path = storage_path
        self.corrections = self._load_corrections()
        self.patterns = defaultdict(int)

    def _load_corrections(self):
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def save_corrections(self):
        with open(self.storage_path, 'w') as f:
            json.dump(self.corrections, f, indent=4)

    def adapt(self, raw_text: str, corrected_text: str):
        """
        Records a correction to learn the user's annunciation.
        """
        if raw_text.strip().lower() != corrected_text.strip().lower():
            self.corrections[raw_text.strip().lower()] = corrected_text.strip().lower()
            self.save_corrections()

    def correct(self, text: str) -> str:
        """
        Applies learned corrections to transcribed text.
        """
        normalized = text.strip().lower()
        return self.corrections.get(normalized, text)

# Global instance for the system
SPEECH_ADAPTOR = SpeechAdaptor()
