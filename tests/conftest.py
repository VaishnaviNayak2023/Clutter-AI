"""Pytest configuration and fixtures."""

import shutil
import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    shutil.rmtree(temp_path, ignore_errors=True)


@pytest.fixture
def sample_files(temp_dir):
    """Create sample files for testing."""
    # Create some sample text files
    (temp_dir / "document1.txt").write_text("This is a test document.")
    (temp_dir / "document2.txt").write_text("This is another test document.")
    (temp_dir / "code.py").write_text("print('Hello, world!')")

    # Create a subdirectory with a file
    subdir = temp_dir / "subfolder"
    subdir.mkdir()
    (subdir / "notes.md").write_text("# Notes\n\nSome markdown content.")

    return temp_dir
