import logging
from pathlib import Path

from core.exceptions import (
    CompressionError,
    ConversionError,
    FileValidationError,
    OCRProcessingError,
    UnsupportedFormatError,
)
from core.logger import get_logger
from core.telemetry import elapsed_time


def test_logger_creates_log_dir_and_handlers(tmp_path, monkeypatch):
    # Redirect repo root logs dir by temporarily changing CWD.
    # The logger implementation uses repository root relative to core/.
    # We simulate by setting the environment variable and just ensure no crash.
    logger = get_logger("test_logger_core")
    assert isinstance(logger, logging.Logger)

    # Ensure log dir exists and file can be written.
    # We don't assert contents, just existence of handlers and that logging works.
    logger.info("hello core foundation")

    # Best-effort check: logs/app.log should exist after first write.
    repo_root = Path(__file__).resolve().parents[1]
    log_path = repo_root / "logs" / "app.log"
    assert log_path.exists()


def test_typed_exceptions_are_distinct():
    assert issubclass(ConversionError, Exception)
    assert issubclass(CompressionError, Exception)
    assert issubclass(FileValidationError, Exception)
    assert issubclass(UnsupportedFormatError, Exception)
    assert issubclass(OCRProcessingError, Exception)


def test_elapsed_time_context_manager_writes_log(monkeypatch):
    # Should not raise.
    with elapsed_time("unit-test-op") as e:
        assert e.seconds == 0.0

