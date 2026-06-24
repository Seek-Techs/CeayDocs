from __future__ import annotations

from core.exceptions import (
    FileValidationError,
    UnsupportedFormatError,
    OCRProcessingError,
    CompressionError,
    ConversionError,
    CeayDocsError,
)


def handle_validation_error(exc: Exception) -> str:
    return "Invalid file or page range."


def handle_unsupported_format_error(exc: Exception) -> str:
    return "The selected file type is not supported."


def handle_ocr_error(exc: Exception) -> str:
    return "OCR processing could not be completed."


def handle_compression_error(exc: Exception) -> str:
    return "PDF compression failed."


def handle_conversion_error(exc: Exception) -> str:
    return "File conversion failed."


def translate_error(exc: Exception) -> str:
    """Translate internal exceptions into user-friendly messages.

    This helper is intentionally conservative and does not expose internal
    details (stack traces, subprocess output, etc.).
    """

    if isinstance(exc, UnsupportedFormatError):
        return handle_unsupported_format_error(exc)
    if isinstance(exc, FileValidationError):
        return handle_validation_error(exc)
    if isinstance(exc, OCRProcessingError):
        return handle_ocr_error(exc)
    if isinstance(exc, CompressionError):
        return handle_compression_error(exc)
    if isinstance(exc, ConversionError):
        return handle_conversion_error(exc)

    if isinstance(exc, CeayDocsError):
        # Unknown CeayDocsError subtype.
        return "Operation failed."

    # For truly unknown errors, keep it generic.
    return "Operation failed."

