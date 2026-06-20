from __future__ import annotations

from core.exceptions import ConversionError
from core.logger import get_logger
from core.telemetry import elapsed_time
from utils.convert import word_to_pdf

logger = get_logger(__name__)


def word_to_pdf_adapter(docx_bytes: bytes) -> bytes:
    """Adapter: bytes -> bytes for DOCX -> PDF.

    Compatibility: wraps existing `utils.convert.word_to_pdf(docx_bytes) -> pdf_bytes`.
    """
    with elapsed_time("operation=word_to_pdf"):
        try:
            logger.info("Starting Word -> PDF conversion")
            out = word_to_pdf(docx_bytes)
            logger.info("Completed Word -> PDF conversion (out_bytes=%d)", len(out))
            return out
        except Exception as e:  # noqa: BLE001
            logger.error("Word -> PDF conversion failed: %s", e)
            raise ConversionError("Word -> PDF conversion failed") from e

