from __future__ import annotations

from core.logger import get_logger
from core.telemetry import elapsed_time
from services.operations.exception_mapper import map_exception_for_operation
from utils.images import pdf_to_images

logger = get_logger(__name__)


def pdf_to_images_adapter_zip(pdf_bytes: bytes) -> bytes:
    """Adapter for PDF -> images (zip bytes)."""
    with elapsed_time("operation=pdf_to_images"):
        try:
            logger.info("Starting pdf_to_images (zip)")
            out = pdf_to_images(pdf_bytes)
            logger.info("Completed pdf_to_images (zip_bytes=%d)", len(out))
            return out
        except Exception as e:  # noqa: BLE001
            mapped = map_exception_for_operation("pdf_to_images", e)
            logger.exception(
                "pdf_to_images failed (mapped=%s original=%s)",
                type(mapped).__name__,
                type(e).__name__,
            )
            raise mapped from e



