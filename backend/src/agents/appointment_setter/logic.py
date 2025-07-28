# backend/src/agents/appointment_setter/logic.py

from typing import List, Dict
from ..base_agent import BaseAgent
from .prompts import APPOINTMENT_SETTER_SYSTEM_PROMPT # <-- IMPORT THIS
from ...services.llm_service import LLMService

class AppointmentSetterAgent(BaseAgent):
    """A voice agent specialized in setting appointments."""

    # We now expect a system_prompt to be passed in.
    def __init__(self, llm_service: LLMService, system_prompt: str = APPOINTMENT_SETTER_SYSTEM_PROMPT):
        self.llm_service = llm_service
        self.system_prompt = system_prompt

    def get_initial_greeting(self) -> str:
        # This could also be made dynamic later
        return "Hi, this is Alex from QuickFix Services calling. Is this a good time to chat for a minute?"

    def process_response(self, user_input: str, conversation_history: List[Dict[str, str]]) -> str:
        """
        Uses the LLM to generate a response based on the conversation.
        """
        messages = [{"role": "system", "content": self.system_prompt}]
        messages.extend(conversation_history)
        messages.append({"role": "user", "content": user_input})
        
        ai_response = self.llm_service.get_response(messages)
        
        return ai_response