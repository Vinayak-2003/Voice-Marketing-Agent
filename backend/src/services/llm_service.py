# backend/src/services/llm_service.py
import ollama
from typing import List, Dict
from ..core.config import settings

class LLMService:
    """A service to interact with a self-hosted Ollama LLM."""

    def __init__(self):
        try:
            self.client = ollama.Client(host=settings.OLLAMA_HOST)
            self.model_name = settings.LLM_MODEL_NAME
            # A quick check to see if the model exists.
            self.client.show(self.model_name)
            print(f"LLMService initialized with model: {self.model_name}")
        except Exception as e:
            print(f"Error initializing LLMService: {e}")
            print("Please ensure Ollama is running and you have pulled the model:")
            print(f"docker exec -it voicegenie_ollama ollama pull {self.model_name}")
            raise

    def get_response(self, messages: List[Dict[str, str]]) -> str:
        """
        Gets a chat completion from the Ollama model.
        """
        try:
            response = self.client.chat(
                model=self.model_name,
                messages=messages
            )
            return response['message']['content']
        except Exception as e:
            print(f"Error communicating with Ollama: {e}")
            return "I'm sorry, I'm having a little trouble thinking right now. Could you please repeat that?"