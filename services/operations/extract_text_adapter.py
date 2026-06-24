from __future__ import annotations

from core.exceptions import ConversionError
from core.logger import get_logger
from core.telemetry import elapsed_time
from services.operations.extract_ops import extract_text_op

from services.operations.exception_mapper import map_exception_for_operation


logger = get_logger(__name__)


def extract_text_adapter(pdf_bytes: bytes) -> str:
    """Adapter: bytes -> str for extracting text from PDFs."""
    with elapsed_time("operation=extract_text"):
        try:
            logger.info("Starting extract_text")
            out = extract_text_op(pdf_bytes)
            logger.info("Completed extract_text (chars=%d)", len(out))
            return out
        except Exception as e:  # noqa: BLE001
            mapped = map_exception_for_operation("extract_text", e)
            logger.error(
                "extract_text failed (mapped=%s original=%s): %s",
                type(mapped).__name__,
                type(e).__name__,
                e,
            )
            raise mapped from e


