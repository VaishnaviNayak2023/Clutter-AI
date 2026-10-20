"""Tests for the scanner service."""

from pathlib import Path

import pytest

from src.ai_clutter_cleaner.exceptions import InvalidDirectoryError
from src.ai_clutter_cleaner.services import scan_folder


def test_scan_folder_valid_directory(sample_files):
    """Test scanning a valid directory."""
    results = scan_folder(sample_files)

    assert len(results) > 0
    assert all(isinstance(f.name, str) for f in results)
    assert all(isinstance(f.path, str) for f in results)
    assert all(f.size > 0 for f in results)


def test_scan_folder_with_hashes(sample_files):
    """Test scanning with hash computation."""
    results = scan_folder(sample_files, compute_hashes=True)

    assert len(results) > 0
    assert all(f.sha256 is not None for f in results)
    assert all(len(f.sha256) == 64 for f in results if f.sha256)


def test_scan_folder_without_hashes(sample_files):
    """Test scanning without hash computation."""
    results = scan_folder(sample_files, compute_hashes=False)

    assert len(results) > 0
    assert all(f.sha256 is None for f in results)


def test_scan_folder_empty_directory(temp_dir):
    """Test scanning an empty directory."""
    results = scan_folder(temp_dir)
    assert len(results) == 0


def test_scan_folder_invalid_directory():
    """Test scanning an invalid directory."""
    with pytest.raises(InvalidDirectoryError):
        scan_folder(Path("/nonexistent/path"))


def test_scan_folder_with_exclusions(sample_files):
    """Test scanning with excluded paths."""
    results = scan_folder(sample_files, excluded_paths=["subfolder"])

    # Files in subfolder should be excluded
    assert not any("subfolder" in f.relative_path for f in results)


def test_scan_folder_can_skip_subdirectories(sample_files):
    """Test that non-recursive scans only include files in the selected directory."""
    results = scan_folder(sample_files, recursive=False)

    assert {file.name for file in results} == {
        "document1.txt",
        "document2.txt",
        "code.py",
    }


def test_scan_folder_with_content_extraction(sample_files):
    """Test scanning with content extraction."""
    results = scan_folder(sample_files, extract_content=True)

    assert len(results) > 0
    # Should not fail even with extraction enabled
