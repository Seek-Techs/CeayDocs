from __future__ import annotations

from core.logger import get_logger
from core.telemetry import elapsed_time
from services.operations.exception_mapper import map_exception_for_operation
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
            mapped = map_exception_for_operation("word_to_pdf", e)
            logger.error(
                "Word -> PDF conversion failed (mapped=%s original=%s): %s",
                type(mapped).__name__,
                type(e).__name__,
                e,
            )
            raise mapped from e


