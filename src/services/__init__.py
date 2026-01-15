"""Services package initialization."""

from .digital_twin_manager import DigitalTwinManager

# Import OpenAI-dependent services only if available
__all__ = ["DigitalTwinManager"]

try:
    from .transcript_processor import TranscriptProcessor
    from .chatbot import PatientChatbot
    __all__.extend(["TranscriptProcessor", "PatientChatbot"])
except ImportError:
    # OpenAI dependencies not available
    pass
