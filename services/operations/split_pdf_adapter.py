from __future__ import annotations

from core.exceptions import ConversionError
from core.logger import get_logger
from core.telemetry import elapsed_time
from services.operations.split_ops import split_pdf_op

from services.operations.exception_mapper import map_exception_for_operation


logger = get_logger(__name__)


def split_pdf_adapter(pdf_bytes: bytes, start: int, end: int) -> bytes:
    """Adapter: bytes -> bytes for splitting PDFs."""
    with elapsed_time("operation=split_pdf"):
        try:
            logger.info("Starting split_pdf (start=%d,end=%d)", start, end)
            out = split_pdf_op(pdf_bytes, start, end)
            logger.info("Completed split_pdf (out_bytes=%d)", len(out))
            return out
        except Exception as e:  # noqa: BLE001
            mapped = map_exception_for_operation("split_pdf", e)
            logger.error(
                "split_pdf failed (mapped=%s original=%s): %s",
                type(mapped).__name__,
                type(e).__name__,
                e,
            )
            raise mapped from e


