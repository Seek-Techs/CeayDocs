# services/pdf_to_word.py
import logging
from utils.convert import pdf_to_word as util_pdf_to_word

logger = logging.getLogger(__name__)

class PdfToWordService:
    """
    Thin service wrapper around the existing utils.convert.pdf_to_word function.

    Responsibilities:
    - Validate input bytes
    - Provide a single call entrypoint for UI/API
    - Central place for future job wiring, logging, timeouts, retries
    
    """

    def execute(self, input_bytes: bytes) -> bytes:
        if not input_bytes:
            raise ValueError("No input bytes provided")

        try:
            result = util_pdf_to_word(input_bytes)
            if result is None:
                raise RuntimeError("Conversion returned no output")
            return result
        except Exception:
            logger.exception("PdfToWordService failed")
            raise
