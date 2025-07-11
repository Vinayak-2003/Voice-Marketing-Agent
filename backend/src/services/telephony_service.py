# backend/src/services/telephony_service.py
# This is a CONCEPTUAL file to illustrate the kinds of actions
# a voice application needs to perform. The `calls.py` router
# implements this logic directly for simplicity.

class TelephonyActionBuilder:
    """
    A helper class to build structured responses for a telephony platform like Asterisk or FreeSWITCH.
    """

    @staticmethod
    def play_audio(file_url: str):
        """Instruction to play an audio file."""
        return {"action": "play", "url": file_url}

    @staticmethod
    def gather_speech(timeout: int = 5, end_on_silence_ms: int = 2000):
        """Instruction to listen for the user to speak."""
        return {
            "action": "gather",
            "params": {
                "timeout": timeout,
                "end_on_silence": f"{end_on_silence_ms}ms"
            }
        }

    @staticmethod
    def hangup():
        """Instruction to end the call."""
        return {"action": "hangup"}