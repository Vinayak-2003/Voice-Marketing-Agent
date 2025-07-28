# backend/src/services/llm_service.py
import ollama
import time
from ..core.config import settings

class LLMService:
    """A service to interact with a self-hosted Ollama LLM with resilient connection."""

    def __init__(self):
        self.client = None
        self.model_name = settings.LLM_MODEL_NAME
        
        # --- THIS IS THE RESILIENT CONNECTION LOGIC ---
        max_retries = 15
        retry_delay = 10  # seconds
        
        for attempt in range(max_retries):
            try:
                print(f"LLMService: Attempting to connect to Ollama at {settings.OLLAMA_HOST} (Attempt {attempt + 1}/{max_retries})...")
                self.client = ollama.Client(host=settings.OLLAMA_HOST)
                # Use a simple, reliable command to check if the service is responsive.
                self.client.list() 
                print("✅ LLMService: Successfully connected to Ollama.")
                return  # Exit the __init__ method on success
            except Exception as e:
                print(f"⚠️ LLMService: Connection failed. Retrying in {retry_delay} seconds...")
                if attempt + 1 == max_retries:
                    print(f"❌ Final attempt failed. Error: {e}")
                    break # Exit loop on final failure
                time.sleep(retry_delay)
        
        # If the loop finishes without returning, we failed to connect.
        print("❌ LLMService: Could not connect to Ollama after multiple retries. The application will not be able to function correctly.")
        raise ConnectionError("Failed to connect to the Ollama service after multiple attempts.")

    def get_response(self, messages):
        """Gets a chat completion from the Ollama model."""
        if not self.client:
            print("❌ LLMService: Client not initialized. Cannot get response.")
            return "I'm sorry, my connection to the language model is not available."
            
        try:
            response = self.client.chat(
                model=self.model_name,
                messages=messages
            )
            return response['message']['content']
        except Exception as e:
            print(f"Error communicating with Ollama: {e}")
            return "I'm sorry, I'm having a little trouble thinking right now."