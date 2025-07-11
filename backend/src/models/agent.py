# backend/src/models/agent.py
from sqlalchemy import Column, Integer, String, Text
from ..core.database import Base

class Agent(Base):
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    system_prompt = Column(Text, nullable=False)
    voice_id = Column(String, default="default_voice") # For future use with different TTS voices