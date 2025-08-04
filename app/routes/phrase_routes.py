from fastapi import APIRouter
import random

router = APIRouter()

# Predefined phrases for liveness detection
PHRASES = [
    "Green apples are sweet",
    "I love sunny mornings",
    "The book is on the table",
    "Clouds are floating in the sky",
    "Technology is evolving fast"
]

@router.get("/generate")
def generate_phrase():
    """Generate a random phrase for liveness detection."""
    phrase = random.choice(PHRASES)
    return {"phrase": phrase}
