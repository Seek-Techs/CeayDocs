from __future__ import annotations

from typing import Optional

from core.exceptions import ConversionError
from core.logger import get_logger
from core.telemetry import elapsed_time
from utils.convert import pdf_to_word

logger = get_logger(__name__)


def pdf_to_word_adapter(pdf_bytes: bytes) -> bytes:
    """Adapter: bytes -> bytes for PDF -> DOCX.

    Compatibility: wraps existing `utils.convert.pdf_to_word(pdf_bytes) -> docx_bytes`.
    """
    with elapsed_time("operation=pdf_to_word"):
        try:
            logger.info("Starting PDF -> Word conversion")
            out_bytes = pdf_to_word(pdf_bytes)
            if not isinstance(out_bytes, (bytes, bytearray)):
                raise ConversionError("pdf_to_word returned non-bytes output")
            out_bytes = bytes(out_bytes)
            logger.info("Completed PDF -> Word conversion (out_bytes=%d)", len(out_bytes))
            return out_bytes
        except Exception as e:  # noqa: BLE001
            logger.error("PDF -> Word conversion failed: %s", e)
            raise ConversionError("PDF -> Word conversion failed") from e

