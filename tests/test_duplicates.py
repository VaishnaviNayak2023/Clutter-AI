"""Tests for the duplicates service."""

from collections import defaultdict

from src.ai_clutter_cleaner.services import scan_folder


def test_exact_duplicate_detection(sample_files):
    """Test that exact duplicates are detected via hash matching."""
    # Create a duplicate file
    duplicate = sample_files / "duplicate.txt"
    duplicate.write_text((sample_files / "document1.txt").read_text())

    # Scan with hash computation
    results = scan_folder(sample_files, compute_hashes=True)

    # Group by hash
    hash_groups = defaultdict(list)
    for file in results:
        if file.sha256:
            hash_groups[file.sha256].append(file)

    # Find duplicate groups
    duplicate_groups = {h: files for h, files in hash_groups.items() if len(files) > 1}

    # Should find at least one duplicate group
    assert len(duplicate_groups) >= 1
    assert any(len(files) == 2 for files in duplicate_groups.values())
