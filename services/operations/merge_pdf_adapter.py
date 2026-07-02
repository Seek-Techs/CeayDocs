from __future__ import annotations

from typing import Iterable

from core.logger import get_logger
from core.telemetry import elapsed_time
from services.operations.exception_mapper import map_exception_for_operation
from services.operations.merge_ops import merge_pdfs_op

logger = get_logger(__name__)


def merge_pdfs_adapter(pdf_bytes_list: Iterable[bytes]) -> bytes:
    """Adapter: bytes[] -> bytes for PDF merging."""
    with elapsed_time("operation=merge_pdfs"):
        try:
            count = (sum(1 for _ in pdf_bytes_list) if not isinstance(pdf_bytes_list, list) else len(pdf_bytes_list))
            logger.info("Starting merge_pdfs (count=%d)", count)

            # Note: if pdf_bytes_list is an iterator, we can't iterate twice. Normalize.
            pdf_list = list(pdf_bytes_list)
            out = merge_pdfs_op(pdf_list)
            logger.info("Completed merge_pdfs (out_bytes=%d)", len(out))
            return out
        except Exception as e:  # noqa: BLE001
            mapped = map_exception_for_operation("merge_pdfs", e)
            logger.error(
                "merge_pdfs failed (mapped=%s original=%s): %s",
                type(mapped).__name__,
                type(e).__name__,
                e,
            )
            raise mapped from e



