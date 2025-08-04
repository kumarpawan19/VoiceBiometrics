# app/services/voice_service.py
from resemblyzer import VoiceEncoder, preprocess_wav
import numpy as np
import soundfile as sf
import io

encoder = VoiceEncoder()

def extract_embedding(audio_bytes: bytes):
    """Convert uploaded audio to voice embedding."""
    wav, _ = sf.read(io.BytesIO(audio_bytes))
    embedding = encoder.embed_utterance(preprocess_wav(wav))
    return embedding
