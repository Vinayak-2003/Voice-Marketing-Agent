# VoiceGenie Developer Project

This project is a backend system for building real-time, AI-powered voice agents for phone automation. It's designed to be self-hosted and uses open-source models to avoid reliance on paid APIs.

## Tech Stack

- **Backend:** Python, FastAPI
- **Database:** PostgreSQL (via Docker)
- **Telephony Integration:** Designed for webhook-based systems (like Asterisk AGI or FreeSWITCH).
- **LLM (Language Model):** [Ollama](https://ollama.ai/) (running models like Mistral, Llama 2)
- **STT (Speech-to-Text):** [OpenAI Whisper](https://github.com/openai/whisper) (self-hosted)
- **TTS (Text-to-Speech):** [Coqui TTS](https://github.com/coqui-ai/TTS) (self-hosted)
- **Containerization:** Docker & Docker Compose

## Project Structure

- `/backend`: The main FastAPI application.
- `/frontend`: (Placeholder) For a future management dashboard.
- `/ai_models`: (Placeholder) For storing downloaded model files.
- `docker-compose.yml`: Orchestrates all services.

## Setup & Running the Project

1.  **Prerequisites:**
    -   [Docker](https://www.docker.com/get-started) and Docker Compose must be installed.

2.  **Configuration:**
    -   Copy the example environment file: `cp .env.example .env`
    -   Review and update the variables in the `.env` file if needed.

3.  **Build and Run Services:**
    -   Start all services in the background: `docker-compose up -d --build`

4.  **Pull AI Models:**
    -   Once the `ollama` container is running, pull the LLM model specified in your `.env` file.
    ```bash
    docker exec -it voicegenie_ollama ollama pull mistral
    ```
    - The Whisper and Coqui TTS models will be downloaded automatically by the backend service on its first run.

5.  **Accessing the API:**
    -   The API will be available at `http://localhost:8000`.
    -   Interactive API documentation (Swagger UI) is at `http://localhost:8000/docs`.

## How it Works

The system operates on a webhook model. A telephony server (like Asterisk) handles the actual phone call and communicates with our backend via HTTP requests.

1.  **Incoming Call:** Asterisk receives a call and sends a webhook to `/api/v1/calls/webhook`.
2.  **Greeting:** The backend generates a welcome message using the TTS service, saves it as a `.wav` file, and responds with instructions for Asterisk to play that file.
3.  **User Speech:** Asterisk records the user's response and sends a new webhook with the audio file.
4.  **Processing:** The backend uses the STT service to transcribe the audio, the LLM service to determine the next response, and the TTS service to generate the new audio.
5.  **Loop:** This cycle repeats until the agent decides to end the call or the user hangs up.