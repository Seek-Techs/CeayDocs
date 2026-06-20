import os
from typing import List


def _get_int(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None:
        return default
    try:
        return int(raw)
    except ValueError:
        return default


def _get_str_list(name: str, default: List[str]) -> List[str]:
    raw = os.getenv(name)
    if not raw:
        return default
    return [x.strip() for x in raw.split(",") if x.strip()]


# File constraints
MAX_FILE_SIZE = _get_int("CEAYDOCS_MAX_FILE_SIZE", 25 * 1024 * 1024)  # 25MB default

# Defaults for image generation/compression
DEFAULT_DPI = _get_int("CEAYDOCS_DEFAULT_DPI", 150)
DEFAULT_QUALITY = _get_int("CEAYDOCS_DEFAULT_QUALITY", 60)

# Supported formats
SUPPORTED_IMAGE_FORMATS = _get_str_list(
    "CEAYDOCS_SUPPORTED_IMAGE_FORMATS",
    ["png", "jpg", "jpeg"],
)
SUPPORTED_DOCUMENT_FORMATS = _get_str_list(
    "CEAYDOCS_SUPPORTED_DOCUMENT_FORMATS",
    ["pdf", "docx"],
)

# Temp directory
TEMP_DIRECTORY = os.getenv("CEAYDOCS_TEMP_DIRECTORY") or None

