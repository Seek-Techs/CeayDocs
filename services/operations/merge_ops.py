from __future__ import annotations

from typing import Iterable

from utils.merge import merge_pdfs



class _BytesFile:
    def __init__(self, data: bytes):
        self._data = data

    def read(self) -> bytes:
        return self._data


def merge_pdfs_op(pdf_bytes_list: Iterable[bytes]) -> bytes:
    filelikes = [_BytesFile(b) for b in pdf_bytes_list]
    merged = merge_pdfs(filelikes)
    # utils.merge.merge_pdfs can (optionally) return True when output_path is provided.
    # In this operation wrapper we always call without output_path, so ensure bytes.
    if isinstance(merged, bool):
        raise RuntimeError("merge_pdfs returned unexpected boolean result")
    return merged


