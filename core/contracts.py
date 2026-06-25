"""Stable operation contracts (byte -> bytes).

This module documents and standardizes how existing utilities should be
invoked when used as operation adapters.

We intentionally do not enforce runtime checking across the codebase yet.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class BytesToBytesOp(Protocol):
    def __call__(self, data: bytes, *args: Any, **kwargs: Any) -> bytes:  # pragma: no cover
        ...


@runtime_checkable
class BytesToStrOp(Protocol):
    def __call__(self, data: bytes, *args: Any, **kwargs: Any) -> str:  # pragma: no cover
        ...


@runtime_checkable
class PathToBoolOp(Protocol):
    def __call__(self, input_path: Path, output_path: Path, *args: Any, **kwargs: Any) -> bool:  # pragma: no cover
        ...


# Documented legacy signatures (informational)
#
# utils.convert.pdf_to_word
#   - pdf_to_word(pdf_bytes: bytes) -> bytes
#   - pdf_to_word(pdf_path: Path|str, output: Path|str) -> bool
#
# utils.convert.word_to_pdf
#   - word_to_pdf(docx_bytes: bytes) -> bytes
#   - word_to_pdf(docx_path: Path|str, output: Path|str) -> bool
#
# utils.merge.merge_pdfs
#   - merge_pdfs(pdf_inputs, output_path=None) -> bytes (when output_path is None)
#   - merge_pdfs(pdf_inputs, output_path=...) -> True
#
# utils.split.split_pdf
#   - current mixed signature; target contract should become: bytes->bytes
#
# utils.extract.extract_text_from_pdf
#   - extract_text_from_pdf(pdf_bytes: bytes) -> str
#
# utils.images.pdf_to_images
#   - pdf_to_images(file-like) -> list[PIL.Image]
#   - pdf_to_images(pdf_bytes: bytes) -> zip bytes
#
# utils.images.images_to_pdf
#   - images_to_pdf(images: iterable[bytes|BytesIO]) -> pdf bytes


@dataclass(frozen=True)
class OperationMetadata:
    name: str
    input_contract: str
    output_contract: str
    description: str = ""


CONTRACT_DEFAULT = OperationMetadata(
    name="bytes_to_bytes",
    input_contract="bytes",
    output_contract="bytes",
    description="Standard operation adapter contract: bytes -> bytes.",
)

