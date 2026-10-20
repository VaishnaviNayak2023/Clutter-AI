"""Tests for the organizer service."""

from pathlib import Path

from src.ai_clutter_cleaner.services.organizer import (
    FileOrganizer,
    propose_destination,
)


def test_propose_destination(temp_dir):
    """Test proposing a destination path."""
    file_path = Path("/some/path/document.pdf")
    category = "Work and Projects"
    root = temp_dir

    destination = propose_destination(file_path, category, root)

    assert destination.name == file_path.name
    assert "Work_and_Projects" in str(destination)


def test_organizer_initialization(temp_dir):
    """Test organizer initialization."""
    organizer = FileOrganizer(temp_dir)
    assert organizer.root_directory == temp_dir.resolve()
    assert len(organizer.operations) == 0


def test_organizer_propose_destination(temp_dir):
    """Test proposing destination through organizer."""
    organizer = FileOrganizer(temp_dir)
    file_path = Path("/some/document.pdf")
    category = "Work and Projects"

    destination = organizer.propose_destination(file_path, category)

    assert destination.name == file_path.name
    assert "Work_and_Projects" in str(destination)


def test_organizer_validate_move_success(temp_dir):
    """Test validating a valid move."""
    organizer = FileOrganizer(temp_dir)

    # Create a test file
    source = temp_dir / "test.txt"
    source.write_text("test content")

    destination = temp_dir / "organized" / "test.txt"

    is_valid, error = organizer.validate_move(source, destination)

    assert is_valid is True
    assert error is None


def test_organizer_validate_move_nonexistent_source(temp_dir):
    """Test validating move with nonexistent source."""
    organizer = FileOrganizer(temp_dir)

    source = temp_dir / "nonexistent.txt"
    destination = temp_dir / "organized" / "test.txt"

    is_valid, error = organizer.validate_move(source, destination)

    assert is_valid is False
    assert "does not exist" in error


def test_organizer_execute_move_dry_run(temp_dir):
    """Test executing a move in dry-run mode."""
    organizer = FileOrganizer(temp_dir)

    # Create a test file
    source = temp_dir / "test.txt"
    source.write_text("test content")

    destination = temp_dir / "organized" / "test.txt"

    operation = organizer.execute_move(source, destination, dry_run=True)

    assert operation.status == "completed"
    assert source.exists()  # File should still be at source
    assert not destination.parent.exists()  # Dry runs must not create destination folders.


def test_organizer_execute_move_actual(temp_dir):
    """Test executing an actual move."""
    organizer = FileOrganizer(temp_dir)

    # Create a test file
    source = temp_dir / "test.txt"
    source.write_text("test content")

    destination = temp_dir / "organized" / "test.txt"

    operation = organizer.execute_move(source, destination, dry_run=False)

    assert operation.status == "completed"
    assert not source.exists()  # File moved from source
    assert destination.exists()  # File at destination


def test_organizer_execute_move_existing_destination(temp_dir):
    """Test executing move when destination already exists."""
    organizer = FileOrganizer(temp_dir)

    # Create source and destination files
    source = temp_dir / "test.txt"
    source.write_text("source content")

    destination = temp_dir / "organized" / "test.txt"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text("existing content")

    operation = organizer.execute_move(source, destination, dry_run=False)

    assert operation.status == "failed"
    assert "already exists" in operation.error_message


def test_organizer_undo_move(temp_dir):
    """Test undoing a move operation."""
    organizer = FileOrganizer(temp_dir)

    # Create and move a file
    source = temp_dir / "test.txt"
    source.write_text("test content")

    destination = temp_dir / "organized" / "test.txt"

    operation = organizer.execute_move(source, destination, dry_run=False)
    assert operation.status == "completed"

    # Undo the move
    undone = organizer.undo_move(operation.operation_id)

    assert undone.status == "undone"
    assert source.exists()  # File back at source
    assert not destination.exists()  # No longer at destination
