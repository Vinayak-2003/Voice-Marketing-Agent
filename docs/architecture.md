# System Architecture

This document provides a high-level overview of the VoiceGenie system architecture. The system is designed around a webhook-based model, where an external telephony server manages the actual phone call and our backend provides the "brains".

## Core Components

1.  **Telephony Server (e.g., Asterisk, FreeSWITCH, Twilio)**: The component that handles the actual PSTN (Public Switched Telephone Network) connection. It manages call states, plays audio, and records user speech. It is considered an external dependency.

2.  **Backend (FastAPI)**: The core of our application. It exposes a webhook that the Telephony Server calls at different stages of the conversation. It's responsible for orchestrating the AI services.

3.  **STT Service (Whisper)**: A service that takes an audio file (the user's speech) and transcribes it into text.

4.  **LLM Service (Ollama)**: Takes the transcribed text and the conversation history to generate the next appropriate response based on a system prompt.

5.  **TTS Service (Coqui TTS)**: Takes the text response from the LLM and synthesizes it into a human-sounding audio file.

6.  **Database (PostgreSQL)**: Stores information about agents, call logs, and conversation history.

## Call Flow Diagram

Here is the typical flow of a single turn in a conversation:

```mermaid
sequenceDiagram
    participant User
    participant Telephony Server
    participant Backend API
    participant STT
    participant LLM
    participant TTS

    User->>+Telephony Server: Speaks ("I'm available Tuesday.")
    Telephony Server->>+Backend API: POST /webhook (with audio file)
    Backend API->>+STT: Transcribe audio
    STT-->>-Backend API: Returns text ("I'm available Tuesday.")
    Backend API->>+LLM: Process text + history
    LLM-->>-Backend API: Returns response text ("Great, I've booked you for Tuesday.")
    Backend API->>+TTS: Synthesize text to audio
    TTS-->>-Backend API: Returns new audio file
    Backend API-->>-Telephony Server: 200 OK (with actions: Play audio file)
    Telephony Server->>-User: Plays audio ("Great, I've booked you...")