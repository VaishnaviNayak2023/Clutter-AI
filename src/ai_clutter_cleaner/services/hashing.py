"""File hashing service for duplicate detection."""

import hashlib
from pathlib import Path


def compute_file_hash(path: Path) -> str:
    """
    Compute SHA-256 hash of a file using chunked reading.

    Args:
        path: Path to the file

    Returns:
        Hexadecimal SHA-256 hash
    """
    digest = hashlib.sha256()
    with open(path, "rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()
