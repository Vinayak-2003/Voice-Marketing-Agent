#!/bin/bash

# This script helps you download the necessary LLM model for the project.
# The STT (Whisper) and TTS (Coqui) models are downloaded automatically by the Python services on first run.

echo "--- VoiceGenie Model Setup ---"
echo ""

# Check if docker is running
if ! docker info > /dev/null 2>&1; then
  echo "❌ Docker does not seem to be running. Please start Docker and try again."
  exit 1
fi

# Check if the ollama container is running
if ! docker ps --filter "name=voicegenie_ollama" --format "{{.Names}}" | grep -q "voicegenie_ollama"; then
  echo "⚠️ The 'voicegenie_ollama' container is not running."
  echo "Please start the services first with: docker-compose up -d"
  exit 1
fi

# Read the model name from the .env file, defaulting to 'mistral'
if [ -f ".env" ]; then
  MODEL_NAME=$(grep LLM_MODEL_NAME .env | cut -d '=' -f2)
else
  MODEL_NAME="mistral"
  echo "⚠️ .env file not found. Defaulting to model: 'mistral'"
fi

echo "✅ Ollama container is running."
echo "🚀 Attempting to pull the LLM model: '$MODEL_NAME'..."
echo "This may take several minutes and download a few gigabytes."
echo ""

docker exec -it voicegenie_ollama ollama pull $MODEL_NAME

echo ""
echo "✅ Model pull command executed."
echo "If there were no errors, the setup is complete!"
echo "The STT and TTS models will be downloaded automatically when the backend API is first used."