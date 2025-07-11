# AI Models

This directory is a placeholder for storing self-hosted AI models. However, the recommended approach is to let the services manage the models themselves. This file provides instructions on how to acquire the necessary models for each service.

---

### 1. LLM (Large Language Model) - Ollama

The backend is configured to use **Ollama** to serve language models like Mistral or Llama 2. You need to pull the model into the Ollama service after it's running.

1.  **Start the Docker services:**
    ```bash
    docker-compose up -d
    ```

2.  **Pull the model:**
    Execute the following command on your host machine. This will connect to the running `voicegenie_ollama` container and download the `mistral` model (or whichever model is specified in your `.env` file).

    ```bash
    docker exec -it voicegenie_ollama ollama pull mistral
    ```
    *This download can be several gigabytes and may take some time.*

---

### 2. STT (Speech-to-Text) - OpenAI Whisper

The `openai-whisper` Python library will **automatically download** the required model the first time the `STTService` is initialized.

-   The model size is configured by the `WHISPER_MODEL_SIZE` variable in your `.env` file (e.g., `base`).
-   The model files will be cached in your user's home directory (e.g., `~/.cache/whisper/`). You do not need to place any files in this directory manually.

---

### 3. TTS (Text-to-Speech) - Coqui TTS

Similar to Whisper, the `TTS` Python library from Coqui AI will **automatically download** the required voice model the first time the `TTSService` is initialized.

-   The model is configured by the `TTS_MODEL_NAME` variable in your `.env` file (e.g., `tts_models/en/ljspeech/vits`).
-   The model files will be downloaded and cached locally (often in `~/AppData/Local/tts/` on Windows or `~/.local/share/tts/` on Linux). You do not need to place any files in this directory manually.