from faster_whisper import WhisperModel
import os

# Initialize model once (singleton-like pattern) to save loading time during requests
# "base" model is fast and good enough for a student project.
model_size = "base"
# Compute type int8 for CPU efficiency. Change to float16 if you have a good GPU.
model = WhisperModel(model_size, device="cpu", compute_type="int8")

def transcribe_audio(audio_path: str) -> str:
    """
    Transcribes audio using local faster-whisper.
    Returns the full transcript as a string.
    """
    segments, info = model.transcribe(audio_path, beam_size=5)
    
    transcript = ""
    for segment in segments:
        transcript += segment.text + " "
        
    return transcript.strip()
