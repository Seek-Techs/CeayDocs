from __future__ import annotations

from core.exceptions import ConversionError
from core.logger import get_logger
from core.telemetry import elapsed_time
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
            logger.error("pdf_to_images failed: %s", e)
            raise ConversionError("PDF -> images failed") from e

