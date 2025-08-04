from fastapi import APIRouter, UploadFile, HTTPException
from app.services.voice_service import extract_embedding
from app.db.mock_db import voice_db
import numpy as np


router = APIRouter()

@router.post("/enroll/{user_id}")
async def enroll_voice(user_id: str, file: UploadFile):
    """Enroll user's voice and store embedding."""
    if not file.filename.endswith(".wav"):
        raise HTTPException(status_code=400, detail="Only .wav files are supported.")

    audio_bytes = await file.read()
    embedding = extract_embedding(audio_bytes)

    # Save embedding in our "DB"
    voice_db[user_id] = embedding.tolist()
    return {"message": f"Voice enrolled successfully for user: {user_id}"}

@router.post("/verify/{user_id}")
async def verify_voice(user_id: str, file: UploadFile):
    """Verify speaker identity using voice similarity only."""
    if user_id not in voice_db:
        raise HTTPException(status_code=404, detail="User not enrolled")

    if not file.filename.endswith(".wav"):
        raise HTTPException(status_code=400, detail="Only .wav files are supported.")

    # Read uploaded audio file
    audio_bytes = await file.read()

    # Extract embeddings
    stored_embedding = np.array(voice_db[user_id])
    new_embedding = extract_embedding(audio_bytes)

    # Cosine similarity
    similarity = np.dot(new_embedding, stored_embedding) / (
        np.linalg.norm(new_embedding) * np.linalg.norm(stored_embedding)
    )

    verified = bool(similarity > 0.85)  # Threshold for speaker match
    return {
        "verified": verified,
        "voice_similarity": round(float(similarity), 3)
    }