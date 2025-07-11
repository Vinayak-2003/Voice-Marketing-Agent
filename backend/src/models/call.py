# backend/src/models/call.py
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from ..core.database import Base

class CallLog(Base):
    __tablename__ = "call_logs"

    id = Column(Integer, primary_key=True, index=True)
    call_sid = Column(String, unique=True, index=True, nullable=False)
    from_number = Column(String, index=True)
    start_time = Column(DateTime(timezone=True), server_default=func.now())
    end_time = Column(DateTime(timezone=True), onupdate=func.now())
    full_transcript = Column(Text)