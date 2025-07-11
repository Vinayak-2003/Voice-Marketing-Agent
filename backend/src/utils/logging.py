# backend/src/utils/logging.py
import logging
import sys

# Configure a basic logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def log_call_event(call_sid: str, event: str, details: dict = None):
    """
    A structured logger for call events.
    """
    message = f"CALL_EVENT: [SID: {call_sid}] [Event: {event}]"
    if details:
        message += f" [Details: {details}]"
    logger.info(message)