# backend/src/api/routes/calls.py
import os
import uuid
from fastapi import APIRouter, Depends, Form, HTTPException, Response
from sqlalchemy.orm import Session
from pydantic import BaseModel
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Gather

from ...core.database import get_db
from ...core.config import settings
from ...services.llm_service import LLMService
from ...services.stt_service import STTService
from ...services.tts_service import TTSService
from ...agents.appointment_setter.logic import AppointmentSetterAgent
from ...models import agent as agent_model

router = APIRouter()

stt_service = STTService()
tts_service = TTSService()
llm_service = LLMService()


@router.post("/webhook")
async def call_webhook(
    db: Session = Depends(get_db),
    agent_id: int = Form(1),
    SpeechResult: str = Form(None),
):
    # --- DYNAMIC AGENT LOADING ---
    db_agent = db.query(agent_model.Agent).filter(agent_model.Agent.id == agent_id).first()
    if not db_agent:
        raise HTTPException(status_code=404, detail=f"Agent with ID {agent_id} not found.")
    agent = AppointmentSetterAgent(llm_service, system_prompt=db_agent.system_prompt)

    # --- TwiML RESPONSE GENERATION ---
    response = VoiceResponse()
    public_url = os.environ.get('PUBLIC_URL')
    if not public_url:
        raise HTTPException(status_code=500, detail="PUBLIC_URL environment variable is not set.")

    if SpeechResult is None:
        # First leg of the call, play the initial greeting
        text_to_speak = agent.get_initial_greeting()
    else:
        # The user has spoken, process their response
        user_transcript = SpeechResult
        print(f"User said: {user_transcript}")
        # Get the AI's next response
        text_to_speak = agent.process_response(user_transcript, conversation_history=[])
        print(f"AI will say: {text_to_speak}")

    # Synthesize the text to an audio file
    filename = f"{uuid.uuid4()}.wav"
    audio_file_path = os.path.join(settings.AUDIO_DIR, filename)
    tts_service.synthesize(text_to_speak, audio_file_path)

    # Construct the public URL for the audio file
    public_audio_url = f"{public_url}/audio/{filename}"

    # Tell Twilio to play the audio file
    response.play(public_audio_url)

    # After playing, listen for the user's next response and send it back to this same webhook
    gather = Gather(input='speech', action=f'/api/v1/calls/webhook?agent_id={agent_id}', speech_timeout='auto', method='POST')
    response.append(gather)

    return Response(content=str(response), media_type="application/xml")


# --- Endpoint to Start a Call ---

class OriginateCallRequest(BaseModel):
    phone_number: str
    agent_id: int

@router.post("/originate")
async def originate_call(request: OriginateCallRequest):
    """
    Receives a request from the frontend and uses Twilio to start a real outbound call.
    """
    print(f"Received request to start a REAL call to: {request.phone_number} with Agent ID: {request.agent_id}")

    account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
    twilio_phone_number = os.environ.get('TWILIO_PHONE_NUMBER')
    public_url = os.environ.get('PUBLIC_URL')

    if not all([account_sid, auth_token, twilio_phone_number, public_url]):
        raise HTTPException(status_code=500, detail="Server is not configured for making calls. TWILIO environment variables are missing.")

    client = Client(account_sid, auth_token)

    try:
        webhook_url_with_agent = f"{public_url}/api/v1/calls/webhook?agent_id={request.agent_id}"
        
        call = client.calls.create(
            to=request.phone_number,
            from_=twilio_phone_number,
            url=webhook_url_with_agent,
            method='POST'  # <-- THIS IS THE CRUCIAL FIX
        )
        print(f"Call successfully initiated with SID: {call.sid}")
        return {"status": "success", "message": f"Successfully initiated call to {request.phone_number}.", "call_sid": call.sid}
    except Exception as e:
        print(f"Error initiating call with Twilio: {e}")
        raise HTTPException(status_code=500, detail=str(e))