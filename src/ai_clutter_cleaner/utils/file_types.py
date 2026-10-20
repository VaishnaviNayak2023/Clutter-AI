"""File type utility functions."""

from pathlib import Path

from src.ai_clutter_cleaner.config import SUPPORTED_EXTENSIONS


def is_supported_file_type(path: Path) -> bool:
    """
    Check if a file has a supported extension.

    Args:
        path: File path

    Returns:
        True if supported, False otherwise
    """
    return path.suffix.lower() in SUPPORTED_EXTENSIONS
