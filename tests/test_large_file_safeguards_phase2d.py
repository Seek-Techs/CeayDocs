from __future__ import annotations

import pytest

from core.config import MAX_FILE_SIZE


def test_safety_config_defined():
    assert isinstance(MAX_FILE_SIZE, int)
    assert MAX_FILE_SIZE > 0

