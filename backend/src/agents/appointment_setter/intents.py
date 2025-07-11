# backend/src/agents/appointment_setter/intents.py
# This file is a placeholder for more advanced intent detection.

def extract_intent(text: str):
    """
    A simple keyword-based intent extractor.
    In a real system, this would use a more sophisticated NLP model or LLM call.
    """
    text = text.lower()
    if "confirm" in text or "sounds good" in text or "yes, please" in text:
        return {"intent": "confirm_appointment", "details": {}}
    if "cancel" in text or "not interested" in text:
        return {"intent": "cancel", "details": {}}
    if "question" in text or "how much" in text:
        return {"intent": "ask_question", "details": {}}
    
    return {"intent": "continue_conversation", "details": {}}