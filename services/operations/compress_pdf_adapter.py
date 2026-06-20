from __future__ import annotations

from core.exceptions import CompressionError
from core.logger import get_logger
from core.telemetry import elapsed_time
from services.operations.compress_ops import compress_pdf_op

logger = get_logger(__name__)


def compress_pdf_adapter(pdf_bytes: bytes) -> bytes:
    """Adapter: bytes -> bytes for PDF compression."""
    with elapsed_time("operation=compress_pdf"):
        try:
            logger.info("Starting compress_pdf")
            out = compress_pdf_op(pdf_bytes)
            logger.info("Completed compress_pdf (out_bytes=%d)", len(out))
            return out
        except Exception as e:  # noqa: BLE001
            logger.error("compress_pdf failed: %s", e)
            raise CompressionError("PDF compression failed") from e

