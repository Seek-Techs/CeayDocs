from __future__ import annotations

from core.logger import get_logger
from core.telemetry import elapsed_time
from services.operations.compress_ops import compress_pdf_op
from services.operations.exception_mapper import map_exception_for_operation

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
            mapped = map_exception_for_operation("compress_pdf", e)
            logger.error(
                "compress_pdf failed (mapped=%s original=%s): %s",
                type(mapped).__name__,
                type(e).__name__,
                e,
            )
            raise mapped from e


