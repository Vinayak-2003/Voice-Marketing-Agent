# backend/src/agents/appointment_setter/logic.py

from typing import List, Dict
from ..base_agent import BaseAgent
from ...services.llm_service import LLMService

# You could rename this class to GenericAgent if you like, but we'll keep it for now.
class AppointmentSetterAgent(BaseAgent):
    """A voice agent that uses a dynamic system prompt passed during initialization."""

    def __init__(self, llm_service: LLMService, system_prompt: str):
        """
        Initializes the agent with a specific LLM service and a dynamic system prompt.

        Args:
            llm_service: The service to interact with the Language Model.
            system_prompt: The system prompt loaded from the database for a specific agent.
        """
        self.llm_service = llm_service
        self.system_prompt = system_prompt

    def get_initial_greeting(self) -> str:
        """
        Returns a generic initial greeting.
        For a more advanced system, this could be the first sentence of an LLM-generated response
        or a specific field stored in the database for the agent.
        """
        return "Hi, this is an AI assistant calling. Is this a good time to talk for a minute?"

    def process_response(self, user_input: str, conversation_history: List[Dict[str, str]]) -> str:
        """
        Processes the user's response by sending the conversation history and the new user input
        to the LLM, guided by the agent's unique system prompt.
        """
        # Construct the message payload for the LLM
        messages = [{"role": "system", "content": self.system_prompt}]
        messages.extend(conversation_history)
        messages.append({"role": "user", "content": user_input})
        
        # Get the AI's response
        ai_response = self.llm_service.get_response(messages)
        
        return ai_response