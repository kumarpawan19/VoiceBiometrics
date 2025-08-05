from fastapi import APIRouter, UploadFile, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.services.voice_service import extract_embedding
from app.db.database import get_db
from app.db.models import VoiceEmbedding
import numpy as np
from app.services.encryption_service import encrypt_embedding, decrypt_embedding

router = APIRouter()

# ---- ENROLL ----
@router.post("/enroll/{user_id}")
async def enroll_voice(user_id: str, file: UploadFile, db: AsyncSession = Depends(get_db)):
    """Enroll user's voice and store encrypted embedding in PostgreSQL (async)."""
    if not file.filename.endswith(".wav"):
        raise HTTPException(status_code=400, detail="Only .wav files are supported.")

    audio_bytes = await file.read()
    embedding = extract_embedding(audio_bytes)
    encrypted = encrypt_embedding(embedding.tolist())  # Always encrypt before saving

    # Query async
    result = await db.execute(select(VoiceEmbedding).filter(VoiceEmbedding.user_id == user_id))
    record = result.scalars().first()

    if record:
        record.embedding = encrypted
    else:
        record = VoiceEmbedding(user_id=user_id, embedding=encrypted)
        db.add(record)

    await db.commit()
    return {"message": f"Voice enrolled successfully for user: {user_id}"}

# ---- VERIFY ----
@router.post("/verify/{user_id}")
async def verify_voice(user_id: str, file: UploadFile, db: AsyncSession = Depends(get_db)):
    """Verify speaker identity using PostgreSQL encrypted embeddings (async)."""
    result = await db.execute(select(VoiceEmbedding).filter(VoiceEmbedding.user_id == user_id))
    record = result.scalars().first()

    if not record:
        raise HTTPException(status_code=404, detail="User not enrolled")

    stored_embedding = np.array(decrypt_embedding(record.embedding))

    if not file.filename.endswith(".wav"):
        raise HTTPException(status_code=400, detail="Only .wav files are supported.")

    audio_bytes = await file.read()
    new_embedding = extract_embedding(audio_bytes)

    similarity = np.dot(new_embedding, stored_embedding) / (
        np.linalg.norm(new_embedding) * np.linalg.norm(stored_embedding)
    )
    verified = bool(similarity > 0.85)

    return {
        "verified": verified,
        "voice_similarity": round(float(similarity), 3)
    }
