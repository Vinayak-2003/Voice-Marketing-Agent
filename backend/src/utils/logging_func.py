# backend/src/utils/logging.py
import logging
import sys

# Configure a basic logger
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def log_call_event(call_sid: str, event: str, details: dict = None, level: str = "info"):
    """
    A structured logger for call events.
    
    Args:
        call_sid (string): unique ID for a specific call when there is a call for the webhook endpoint from twilio
        event (string): short and machine-readable name for what event just happened
        details (dictionary): data payload for an event, stores actual information
        level (string): logging level like info, error
        
    """
    message = f"CALL_EVENT: [SID: {call_sid}] [Event: {event}]"
    if details:
        message += f" [Details: {details}]"

    log_method = getattr(logger, level.lower(), logger.info)
    log_method(message)
