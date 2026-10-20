"""Tests for the hashing service."""


from src.ai_clutter_cleaner.services import compute_file_hash


def test_compute_file_hash(sample_files):
    """Test computing SHA-256 hash of a file."""
    file1 = sample_files / "document1.txt"
    file2 = sample_files / "document2.txt"

    hash1 = compute_file_hash(file1)
    hash2 = compute_file_hash(file2)

    assert isinstance(hash1, str)
    assert len(hash1) == 64  # SHA-256 produces 64 hex characters
    assert hash1 != hash2  # Different files should have different hashes


def test_compute_file_hash_identical_files(temp_dir):
    """Test that identical files produce the same hash."""
    file1 = temp_dir / "duplicate1.txt"
    file2 = temp_dir / "duplicate2.txt"

    content = "Same content"
    file1.write_text(content)
    file2.write_text(content)

    hash1 = compute_file_hash(file1)
    hash2 = compute_file_hash(file2)

    assert hash1 == hash2
