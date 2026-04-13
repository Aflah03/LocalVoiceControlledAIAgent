import os
from faster_whisper import WhisperModel
import numpy as np
import sounddevice as sd

class STTHandler:
    def __init__(self, model_size="base"):
        """
        Initializes the Whisper model.
        model_size options: "tiny", "base", "small", "medium", "large-v3"
        """
        print(f"Loading Whisper model '{model_size}'... This may take a moment.")
        self.model = WhisperModel(model_size, device="cpu", compute_type="int8")
        print("Whisper model loaded successfully.")

    def transcribe_file(self, audio_path: str) -> str:
        """
        Transcribes an audio file from a given path.
        """
        try:
            segments, info = self.model.transcribe(audio_path, beam_size=5)
            text = " ".join([segment.text for segment in segments])
            return text.strip()
        except Exception as e:
            return f"Error transcribing file: {str(e)}"

    def transcribe_live(self, duration: int = 5, fs: int = 16000) -> str:
        """
        Records audio from the microphone for a set duration and transcribes it.
        """
        try:
            print(f"Recording for {duration} seconds...")
            # Record audio
            recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float32')
            sd.wait()  # Wait until recording is finished

            # Flatten the array for Whisper
            audio_data = recording.flatten()

            segments, info = self.model.transcribe(audio_data, beam_size=5)
            text = " ".join([segment.text for segment in segments])
            return text.strip()
        except Exception as e:
            return f"Error during live recording/transcription: {str(e)}"

if __name__ == "__main__":
    # Simple smoke test
    stt = STTHandler()
    print("STT Handler initialized. Ready for testing.")
