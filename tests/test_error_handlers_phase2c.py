from __future__ import annotations

import pytest

from core.error_handlers import translate_error
from core.exceptions import (
    FileValidationError,
    UnsupportedFormatError,
    OCRProcessingError,
    CompressionError,
    ConversionError,
)


@pytest.mark.parametrize(
    "exc, expected",
    [
        (FileValidationError("x"), "Invalid file or page range."),
        (UnsupportedFormatError("x"), "The selected file type is not supported."),
        (OCRProcessingError("x"), "OCR processing could not be completed."),
        (CompressionError("x"), "PDF compression failed."),
        (ConversionError("x"), "File conversion failed."),
    ],
)
def test_translate_error_known_types(exc, expected):
    assert translate_error(exc) == expected


def test_translate_error_unknown():
    assert translate_error(RuntimeError("boom")) == "Operation failed."

