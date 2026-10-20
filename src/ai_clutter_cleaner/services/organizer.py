"""File organization service."""

import os
import shutil
import uuid
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Literal

from src.ai_clutter_cleaner.utils.paths import is_path_safe


@dataclass
class FileMoveOperation:
    """Represents a file move operation."""

    operation_id: str
    source_path: Path
    destination_path: Path
    status: Literal["pending", "completed", "failed", "undone"]
    error_message: str | None = None
    created_at: datetime | None = None
    completed_at: datetime | None = None
    undone_at: datetime | None = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


class FileOrganizer:
    """Handle safe file organization operations."""

    def __init__(self, root_directory: Path):
        """
        Initialize the organizer.

        Args:
            root_directory: Root directory for organized files
        """
        self.root_directory = root_directory.resolve()
        self.operations: list[FileMoveOperation] = []

    def propose_destination(
        self, file_path: Path, category: str, preserve_structure: bool = False
    ) -> Path:
        """
        Propose a destination path for a file based on its category.

        Args:
            file_path: Original file path
            category: Predicted category
            preserve_structure: Whether to preserve relative path structure

        Returns:
            Proposed destination path
        """
        # Sanitize category name for directory
        safe_category = category.replace(" ", "_").replace("/", "_")

        if preserve_structure:
            # Preserve relative directory structure
            relative_parent = file_path.parent.name if file_path.parent != Path(".") else ""
            category_dir = self.root_directory / safe_category / relative_parent
        else:
            category_dir = self.root_directory / safe_category

        return category_dir / file_path.name

    def validate_move(
        self, source: Path, destination: Path, root_check: Path | None = None
    ) -> tuple[bool, str | None]:
        """
        Validate a file move operation.

        Args:
            source: Source file path
            destination: Destination file path
            root_check: Root directory to validate against (optional)

        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check source exists
        if not source.exists():
            return False, f"Source file does not exist: {source}"

        # Check source is a file
        if not source.is_file():
            return False, f"Source is not a file: {source}"

        # Check source is inside root if specified
        if root_check and not is_path_safe(source, root_check):
            return False, "Source is outside authorized root directory"

        # Check destination is inside root if specified
        if root_check and not is_path_safe(destination, root_check):
            return False, "Destination is outside authorized root directory"

        # Check destination doesn't already exist
        if destination.exists():
            return False, f"Destination already exists: {destination}"

        # Validate the nearest existing ancestor without creating directories.
        parent = destination.parent
        while not parent.exists() and parent != parent.parent:
            parent = parent.parent
        if not parent.is_dir():
            return False, "Destination parent is not a directory"
        if not os.access(parent, os.W_OK):
            return False, "Destination parent is not writable"

        return True, None

    def execute_move(
        self,
        source: Path,
        destination: Path,
        dry_run: bool = False,
        root_check: Path | None = None,
    ) -> FileMoveOperation:
        """
        Execute a file move operation.

        Args:
            source: Source file path
            destination: Destination file path
            dry_run: If True, only validate without moving
            root_check: Root directory to validate against

        Returns:
            FileMoveOperation with results
        """
        operation_id = str(uuid.uuid4())
        operation = FileMoveOperation(
            operation_id=operation_id,
            source_path=source,
            destination_path=destination,
            status="pending",
        )

        # Validate
        is_valid, error_msg = self.validate_move(source, destination, root_check)

        if not is_valid:
            operation.status = "failed"
            operation.error_message = error_msg
            operation.completed_at = datetime.now()
            self.operations.append(operation)
            return operation

        if dry_run:
            operation.status = "completed"
            operation.completed_at = datetime.now()
            self.operations.append(operation)
            return operation

        # Execute the move
        try:
            # Ensure destination directory exists
            destination.parent.mkdir(parents=True, exist_ok=True)

            # Move the file
            shutil.move(str(source), str(destination))

            operation.status = "completed"
            operation.completed_at = datetime.now()
        except Exception as e:
            operation.status = "failed"
            operation.error_message = str(e)
            operation.completed_at = datetime.now()

        self.operations.append(operation)
        return operation

    def undo_move(self, operation_id: str) -> FileMoveOperation | None:
        """
        Undo a file move operation.

        Args:
            operation_id: ID of the operation to undo

        Returns:
            Updated FileMoveOperation or None if not found
        """
        # Find the operation
        operation = None
        for op in self.operations:
            if op.operation_id == operation_id:
                operation = op
                break

        if not operation:
            return None

        # Check if undoable
        if operation.status != "completed":
            return operation

        # Check if source still exists at destination
        if not operation.destination_path.exists():
            operation.error_message = "Destination file no longer exists"
            return operation

        # Check if source location is now occupied
        if operation.source_path.exists():
            operation.error_message = "Source location is now occupied"
            return operation

        try:
            # Move back
            shutil.move(str(operation.destination_path), str(operation.source_path))

            operation.status = "undone"
            operation.undone_at = datetime.now()
        except Exception as e:
            operation.error_message = f"Undo failed: {e}"

        return operation

    def batch_move(
        self,
        moves: list[tuple[Path, Path]],
        dry_run: bool = False,
        root_check: Path | None = None,
    ) -> list[FileMoveOperation]:
        """
        Execute multiple file move operations.

        Args:
            moves: List of (source, destination) tuples
            dry_run: If True, only validate without moving
            root_check: Root directory to validate against

        Returns:
            List of FileMoveOperation results
        """
        results = []

        for source, destination in moves:
            result = self.execute_move(source, destination, dry_run, root_check)
            results.append(result)

        return results


def propose_destination(file_path: Path, category: str, root: Path) -> Path:
    """
    Propose a destination path for a file based on its category.

    Args:
        file_path: Original file path
        category: Predicted category
        root: Root organization directory

    Returns:
        Proposed destination path
    """
    organizer = FileOrganizer(root)
    return organizer.propose_destination(file_path, category)
