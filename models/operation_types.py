from __future__ import annotations


class OperationType:
    """Central operation type constants.

    These are plain strings to avoid Enum breakages and keep it lightweight.
    """

    PDF_TO_WORD = "PDF_TO_WORD"
    WORD_TO_PDF = "WORD_TO_PDF"
    MERGE_PDF = "MERGE_PDF"
    SPLIT_PDF = "SPLIT_PDF"
    COMPRESS_PDF = "COMPRESS_PDF"
    EXTRACT_TEXT = "EXTRACT_TEXT"
    PDF_TO_IMAGE = "PDF_TO_IMAGE"
    IMAGE_TO_PDF = "IMAGE_TO_PDF"

    # Future-ready (declared only)
    OCR = "OCR"
    IMAGE_COMPRESSION = "IMAGE_COMPRESSION"
    IMAGE_RESIZE = "IMAGE_RESIZE"
    WATERMARK = "WATERMARK"
    ROTATE = "ROTATE"
    SIGN = "SIGN"

