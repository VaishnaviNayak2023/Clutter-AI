"""Tests for the extractor service."""

from pathlib import Path

import pytest

from src.ai_clutter_cleaner.exceptions import ExtractionError
from src.ai_clutter_cleaner.services import extract_text


def test_extract_text_plain_text(sample_files):
    """Test extracting text from a plain text file."""
    txt_file = sample_files / "document1.txt"
    text = extract_text(txt_file)

    assert "test document" in text


def test_extract_text_markdown(sample_files):
    """Test extracting text from a markdown file."""
    md_file = sample_files / "subfolder" / "notes.md"
    text = extract_text(md_file)

    assert "Notes" in text


def test_extract_text_csv(sample_files):
    """Test extracting text from a CSV file."""
    csv_file = sample_files / "data.csv"
    csv_file.write_text("name,age\nJohn,30\nJane,25")

    text = extract_text(csv_file)
    assert "John" in text
    assert "Jane" in text


def test_extract_text_json(sample_files):
    """Test extracting text from a JSON file."""
    json_file = sample_files / "config.json"
    json_file.write_text('{"key": "value", "number": 42}')

    text = extract_text(json_file)
    assert "key" in text
    assert "value" in text


def test_extract_text_python(sample_files):
    """Test extracting text from a Python file."""
    py_file = sample_files / "code.py"
    text = extract_text(py_file)

    assert "Hello" in text or "print" in text


def test_extract_text_empty_file(temp_dir):
    """Test extracting text from an empty file."""
    empty_file = temp_dir / "empty.txt"
    empty_file.write_text("")

    text = extract_text(empty_file)
    assert text == ""


def test_extract_text_nonexistent_file():
    """Test extracting text from a nonexistent file."""
    with pytest.raises(ExtractionError):
        extract_text(Path("/nonexistent/file.txt"))
