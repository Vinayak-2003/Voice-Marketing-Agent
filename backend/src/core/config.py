# backend/src/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8')

    # Database
    DATABASE_URL: str

    # AI Services
    OLLAMA_HOST: str
    LLM_MODEL_NAME: str
    WHISPER_MODEL_SIZE: str
    TTS_MODEL_NAME: str

    # App
    SECRET_KEY: str
    
    # --- NEW: Shared directory path ---
    AUDIO_DIR: str = "/app/audio_files"


# Create a single instance of the settings to be imported by other modules
settings = Settings()

# Ensure the audio directory exists
os.makedirs(settings.AUDIO_DIR, exist_ok=True)