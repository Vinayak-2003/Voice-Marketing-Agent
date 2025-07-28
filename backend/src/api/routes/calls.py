# backend/src/api/routes/calls.py
import os
import uuid
from fastapi import APIRouter, Depends, Form, File, UploadFile, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel

from ...core.database import get_db
from ...services.llm_service import LLMService
from ...services.stt_service import STTService
from ...services.tts_service import TTSService
from ...services.telephony_service import twilio_service
from ...agents.appointment_setter.logic import AppointmentSetterAgent
from ...models import agent as agent_model

router = APIRouter()

# Service Initialization
stt_service = STTService()
tts_service = TTSService()
llm_service = LLMService()

AUDIO_DIR = "/app/audio_files"
os.makedirs(AUDIO_DIR, exist_ok=True)

# This class defines the expected JSON format for the originate call request.
class OriginateCallRequest(BaseModel):
    to_number: str
    agent_id: int

@router.post("/originate")
def originate_call(request: OriginateCallRequest, db: Session = Depends(get_db)):
    # Check if the agent exists before starting the call
    db_agent = db.query(agent_model.Agent).filter(agent_model.Agent.id == request.agent_id).first()
    if not db_agent:
        raise HTTPException(status_code=404, detail=f"Agent with ID {request.agent_id} not found.")

    try:
        result = twilio_service.originate_call(
            to_number=request.to_number,
            agent_id=request.agent_id
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to initiate call. Error: {str(e)}")


@router.post("/webhook")
async def call_webhook(
    db: Session = Depends(get_db),
    agent_id: int = Query(...), 
    call_sid: str = Form(...),
    from_number: str = Form(...),
    speech_result: UploadFile = File(None)
):
    db_agent = db.query(agent_model.Agent).filter(agent_model.Agent.id == agent_id).first()
    if not db_agent:
        raise HTTPException(status_code=404, detail=f"Agent with ID {agent_id} not found for this call.")

    agent = AppointmentSetterAgent(llm_service=llm_service, system_prompt=db_agent.system_prompt)
    
    conversation_history = [] 

    if speech_result is None:
        greeting_text = agent.get_initial_greeting()
        # NOTE: This response needs to be in proper TwiML format for Twilio to work.
        # This is a conceptual response.
        return f'<Response><Say>{greeting_text}</Say><Gather input="speech" action="/api/v1/calls/webhook?agent_id={agent_id}"/></Response>'
    else:
        user_audio_path = os.path.join(AUDIO_DIR, f"{call_sid}_{uuid.uuid4()}.wav")
        with open(user_audio_path, "wb") as buffer:
            buffer.write(await speech_result.read())

        user_transcript = stt_service.transcribe(user_audio_path)
        ai_response_text = agent.process_response(user_transcript, conversation_history)
        
        if "goodbye" in ai_response_text.lower():
            return f'<Response><Say>{ai_response_text}</Say><Hangup/></Response>'
        else:
            return f'<Response><Say>{ai_response_text}</Say><Gather input="speech" action="/api/v1/calls/webhook?agent_id={agent_id}"/></Response>'