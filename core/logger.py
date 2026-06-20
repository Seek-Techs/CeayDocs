import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from typing import Optional


def _ensure_log_dir() -> str:
    # logs/ is at repository root (one level above this file's directory)
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    log_dir = os.path.join(repo_root, "logs")
    os.makedirs(log_dir, exist_ok=True)
    return log_dir


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Return a configured logger.

    Configuration is intentionally lightweight and safe to call multiple times.
    """
    logger_name = name or "ceaydocs"
    logger = logging.getLogger(logger_name)

    # Prevent duplicate handlers if get_logger() is called multiple times.
    if getattr(logger, "_ceaydocs_configured", False):
        return logger

    logger.setLevel(logging.INFO)

    log_dir = _ensure_log_dir()
    log_path = os.path.join(log_dir, "app.log")

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = RotatingFileHandler(
        log_path,
        maxBytes=2 * 1024 * 1024,  # 2MB
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    logger.propagate = False

    logger._ceaydocs_configured = True  # type: ignore[attr-defined]
    return logger

