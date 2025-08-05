from sqlalchemy import Column, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class VoiceEmbedding(Base):
    __tablename__ = "voice_embeddings"
    user_id = Column(String, primary_key=True, index=True)
    embedding = Column(Text, nullable=False)  # ✅ Encrypted embedding stored as TEXT
