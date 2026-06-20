from __future__ import annotations

from core.exceptions import ConversionError
from core.logger import get_logger
from core.telemetry import elapsed_time
from services.operations.images_ops import images_to_pdf_op

logger = get_logger(__name__)


def images_to_pdf_adapter(image_bytes_list: list[bytes]) -> bytes:
    """Adapter: bytes[] -> bytes for images -> PDF."""
    with elapsed_time("operation=images_to_pdf"):
        try:
            logger.info("Starting images_to_pdf (count=%d)", len(image_bytes_list))
            out = images_to_pdf_op(image_bytes_list)
            logger.info("Completed images_to_pdf (out_bytes=%d)", len(out))
            return out
        except Exception as e:  # noqa: BLE001
            logger.error("images_to_pdf failed: %s", e)
            raise ConversionError("Images -> PDF failed") from e

