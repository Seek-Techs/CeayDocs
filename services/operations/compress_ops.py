from __future__ import annotations

from utils.compress import compress_pdf


class _BytesFile:
    def __init__(self, data: bytes):
        self._data = data

    def read(self) -> bytes:
        return self._data


def compress_pdf_op(pdf_bytes: bytes) -> bytes:
    return compress_pdf(_BytesFile(pdf_bytes))

