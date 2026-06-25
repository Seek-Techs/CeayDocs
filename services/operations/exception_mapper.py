from __future__ import annotations

from core.exceptions import (
    CeayDocsError,
    CompressionError,
    ConversionError,
    FileValidationError,
    OCRProcessingError,
    UnsupportedFormatError,
)


def map_exception_for_operation(operation: str, original: Exception) -> CeayDocsError:

    """Map low-level exceptions to typed core exceptions.

    Adapter-layer hardening contract:
    - Prevent raw exceptions from leaking outside adapters.
    - Prefer fine-grained typing when we can safely infer intent.
    - Be conservative for unknown/unmatched exceptions.

    Backward compatibility:
    - We keep the existing default behavior (ConversionError) when we cannot
      confidently classify the failure, except for compression operations
      where CompressionError is generally the safer default.
    """


    msg = str(original)
    msg_lower = msg.lower()

    # File system / missing inputs
    if isinstance(original, FileNotFoundError):
        return FileValidationError(msg or "File not found")

    # Invalid arguments / page ranges / malformed inputs
    # (ValueError is commonly used by upstream libs for invalid arguments.)
    if isinstance(original, ValueError):
        return FileValidationError(msg or "Invalid input")

    def _contains_any(haystack: str, needles: set[str]) -> bool:
        return any(n in haystack for n in needles)

    # Unsupported formats (extensions / MIME / explicit unsupported)
    unsupported_markers = {
        "unsupported",
        "not supported",
        "unsupported format",
        "mime",
        "content-type",
        "content type",
        "filetype",
        "extension",
        "ext=",
        "allowed formats",
        "supported formats",
    }
    if _contains_any(msg_lower, unsupported_markers) or (
        "unknown" in msg_lower and "pdf" not in msg_lower
    ):
        return UnsupportedFormatError(msg or "Unsupported format")

    # Invalid page ranges / range parsing problems
    # Typical indicators vary by library; we match common keywords.
    page_range_markers = {
        "invalid page",
        "page range",
        "page-range",
        "start page",
        "end page",
        "start must be",
        "end must be",
        "out of bounds",
        "out of range",
        "start>",
        "end<",
    }
    if _contains_any(msg_lower, page_range_markers) or (
        "start" in msg_lower and "end" in msg_lower and "page" in msg_lower
    ):
        return FileValidationError(msg or "Invalid page range")

    # Corrupt PDFs / damaged inputs
    corrupt_markers = {
        "corrupt",
        "damaged",
        "broken",
        "cannot read",
        "unable to read",
        "syntax error",
        "startxref",
        "xref",
        "pdf header",
        "encrypted",
        "unable to decrypt",
    }
    if _contains_any(msg_lower, corrupt_markers):
        # Treat as conversion-like failure from caller perspective.
        return ConversionError(msg or "Corrupt PDF")

    # OCR failures
    if operation in {"extract_text", "extract_ocr", "ocr", "pdf_to_text"}:
        ocr_markers = {
            "ocr",
            "tesseract",
            "traineddata",
            "failed to initialize",
            "no words found",
        }
        if _contains_any(msg_lower, ocr_markers):
            return OCRProcessingError(msg or "OCR failed")

    # Ghostscript failures (compression pipeline)
    if operation in {"compress_pdf", "compression", "pdf_compress"}:
        gs_markers = {
            "ghostscript",
            "gswin",
            "gswin64c",
            "gswin32c",
            "\"gs\"",
            " gs ",
            "subprocess",
            "exit code",
            "non-zero",
            "command failed",
        }
        if _contains_any(msg_lower, gs_markers) or "gs" in msg_lower:
            return CompressionError(msg or "PDF compression failed")

    # LibreOffice/soffice failures (word conversion pipeline)
    if operation in {"pdf_to_word", "word_to_pdf", "libreoffice", "soffice", "convert_word"}:
        lo_markers = {
            "libreoffice",
            "soffice",
            "uno",
            "headless",
            "subprocess",
            "exit status",
            "exit code",
        }
        if _contains_any(msg_lower, lo_markers):
            return ConversionError(msg or "Word conversion failed")

    # If we can tell operation family, choose safe default.
    compression_ops = {"compress_pdf", "compression", "pdf_compress"}
    if operation in compression_ops:
        return CompressionError(msg or "Operation failed")

    return ConversionError(msg or "Operation failed")


