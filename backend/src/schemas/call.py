# backend/src/schemas/call.py
from pydantic import BaseModel
from datetime import datetime

class CallLogBase(BaseModel):
    call_sid: str
    from_number: str
    full_transcript: str | None = None

class CallLogCreate(CallLogBase):
    pass

class CallLog(CallLogBase):
    id: int
    start_time: datetime
    end_time: datetime | None = None

    class Config:
        from_attributes = True # Pydantic v2 name for orm_mode