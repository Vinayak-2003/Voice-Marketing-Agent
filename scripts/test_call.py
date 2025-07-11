# scripts/test_call.py
"""
A script to test the backend's call webhook endpoint.

This simulates the requests that a telephony server (like Asterisk) would make.

Prerequisites:
- The backend server must be running.
- You need to install the `requests` library:
  pip install requests

Usage:
- To simulate the start of a call:
  python scripts/test_call.py
- To simulate a user responding with speech to a specific agent:
  python scripts/test_call.py --with-audio --agent-id 1
"""
import requests
import uuid
import wave
import argparse

# --- Configuration ---
BASE_URL = "http://localhost:8000/api/v1"
WEBHOOK_URL = f"{BASE_URL}/calls/webhook"

# --- Helper Function to create a dummy WAV file ---
def create_dummy_wav(filename="dummy_audio.wav"):
    """Creates a short, silent WAV file for testing uploads."""
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)       # Mono
        wf.setsampwidth(2)       # 16-bit
        wf.setframerate(16000)   # 16kHz sample rate
        for _ in range(16000):
            wf.writeframesraw(b'\x00\x00')
    print(f"Created dummy audio file: {filename}")
    return filename

def test_initial_call(agent_id: int):
    """Simulates the first webhook hit when a call is initiated."""
    print(f"--- 1. Testing Initial Call (Agent ID: {agent_id}) ---")
    
    call_sid = f"TEST_SID_{uuid.uuid4()}"
    from_number = "+15559998888"

    payload = {
        'call_sid': call_sid,
        'from_number': from_number,
        'agent_id': agent_id,
    }

    try:
        response = requests.post(WEBHOOK_URL, data=payload)
        response.raise_for_status()
        print(f"Status Code: {response.status_code}")
        print("Response JSON:")
        print(response.json())
        print("✅ Initial call test successful.")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error during initial call test: {e}")

def test_subsequent_call_with_audio(agent_id: int):
    """Simulates a webhook hit where the user has spoken."""
    print(f"\n--- 2. Testing Call with User Speech (Agent ID: {agent_id}) ---")
    
    call_sid = f"TEST_SID_{uuid.uuid4()}"
    from_number = "+15559998888"
    audio_file = create_dummy_wav()

    # --- ADD THE AGENT ID TO THE PAYLOAD ---
    payload = {
        'call_sid': call_sid,
        'from_number': from_number,
        'agent_id': agent_id
    }

    try:
        with open(audio_file, 'rb') as f:
            files = {'speech_result': (audio_file, f, 'audio/wav')}
            response = requests.post(WEBHOOK_URL, data=payload, files=files)
            response.raise_for_status()

        print(f"Status Code: {response.status_code}")
        print("Response JSON:")
        print(response.json())
        print("✅ Subsequent call test successful.")

    except requests.exceptions.RequestException as e:
        print(f"❌ Error during subsequent call test: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test the VoiceGenie call webhook.")
    parser.add_argument(
        '--with-audio',
        action='store_true',
        help="Simulate a call with an audio response from the user."
    )
    parser.add_argument(
        "--agent-id",
        type=int,
        default=1,
        help="The ID of the agent to test.",
    )
    
    args = parser.parse_args()

    if args.with_audio:
        test_subsequent_call_with_audio(args.agent_id)
    else:
        test_initial_call(args.agent_id)