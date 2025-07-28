# backend/src/services/llm_service.py
import ollama
import time
from ..core.config import settings

class LLMService:
    """A service to interact with a self-hosted Ollama LLM with resilient connection."""

    def __init__(self):
        self.client = None
        # This correctly reads 'tinylama' from your .env file
        self.model_name = settings.LLM_MODEL_NAME
        
        # ... (the resilient connection logic remains the same) ...
        max_retries = 15
        retry_delay = 10
        for attempt in range(max_retries):
            try:
                print(f"LLMService: Attempting to connect to Ollama at {settings.OLLAMA_HOST} (Attempt {attempt + 1}/{max_retries})...")
                self.client = ollama.Client(host=settings.OLLAMA_HOST)
                self.client.list() 
                print("✅ LLMService: Successfully connected to Ollama.")
                return
            except Exception as e:
                print(f"⚠️ LLMService: Connection failed. Retrying in {retry_delay} seconds...")
                if attempt + 1 == max_retries:
                    print(f"❌ Final attempt failed. Error: {e}")
                    break
                time.sleep(retry_delay)
        raise ConnectionError("Failed to connect to the Ollama service after multiple attempts.")

    def get_response(self, messages):
        """Gets a chat completion from the Ollama model."""
        if not self.client:
            return "I'm sorry, my connection to the language model is not available."
            
        try:
            response = self.client.chat(
                # --- THIS IS THE CRITICAL FIX ---
                # Changed from a hardcoded "mistral" to the configured model name
                model=self.model_name,
                # ---------------------------------
                messages=messages
            )
            return response['message']['content']
        except Exception as e:
            print(f"Error communicating with Ollama: {e}")
            return "I'm sorry, I'm having a little trouble thinking right now."