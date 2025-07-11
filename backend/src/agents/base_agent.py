# backend/src/agents/base_agent.py
from abc import ABC, abstractmethod
from typing import List, Dict

class BaseAgent(ABC):
    """Abstract Base Class for all voice agents."""

    @abstractmethod
    def get_initial_greeting(self) -> str:
        """Returns the first thing the agent says when a call connects."""
        pass

    @abstractmethod
    def process_response(self, user_input: str, conversation_history: List[Dict[str, str]]) -> str:
        """
        Processes the user's transcribed input and returns the agent's next response.
        
        Args:
            user_input: The text transcribed from the user's speech.
            conversation_history: A list of previous turns in the conversation.
        
        Returns:
            The text of the agent's response.
        """
        pass