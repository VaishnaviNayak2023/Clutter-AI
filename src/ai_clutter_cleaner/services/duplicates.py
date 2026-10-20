"""Duplicate detection service."""

from collections import defaultdict
from pathlib import Path

from src.ai_clutter_cleaner.services.hashing import compute_file_hash


def find_exact_duplicates(files: list[Path]) -> dict[str, list[Path]]:
    """
    Group files by SHA-256 hash to find exact duplicates.

    Args:
        files: List of file paths

    Returns:
        Dictionary mapping hash to list of file paths
    """
    hash_map = defaultdict(list)

    for file_path in files:
        try:
            file_hash = compute_file_hash(file_path)
            hash_map[file_hash].append(file_path)
        except OSError:
            continue

    # Return only groups with more than one file
    return {h: paths for h, paths in hash_map.items() if len(paths) > 1}
