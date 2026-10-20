"""File scanning service."""

from collections.abc import Callable
from pathlib import Path

from src.ai_clutter_cleaner.config import SUPPORTED_EXTENSIONS
from src.ai_clutter_cleaner.database.repositories import FileRepository
from src.ai_clutter_cleaner.exceptions import InvalidDirectoryError
from src.ai_clutter_cleaner.models import FileMetadata
from src.ai_clutter_cleaner.services.extractor import extract_text
from src.ai_clutter_cleaner.services.hashing import compute_file_hash


def scan_folder(
    folder: Path,
    excluded_paths: list[str] | None = None,
    compute_hashes: bool = True,
    extract_content: bool = False,
    progress_callback: Callable[[int, int], None] | None = None,
    recursive: bool = True,
) -> list[FileMetadata]:
    """
    Scan a folder recursively and collect metadata for supported files.

    Args:
        folder: Path to the folder to scan
        excluded_paths: List of path patterns to exclude
        compute_hashes: Whether to compute SHA-256 hashes
        extract_content: Whether to extract text content from documents
        progress_callback: Optional callback for progress updates (current, total)

    Returns:
        List of FileMetadata objects

    Raises:
        InvalidDirectoryError: If the folder is invalid or inaccessible
    """
    folder = folder.resolve()
    if not folder.is_dir():
        raise InvalidDirectoryError(f"Not a valid directory: {folder}")

    excluded_paths = excluded_paths or []
    results = []

    # First pass: collect all file paths
    file_paths = []
    paths = folder.rglob("*") if recursive else folder.iterdir()
    for path in paths:
        if not path.is_file():
            continue

        if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        # Check if path is in excluded list
        if any(excluded in str(path) for excluded in excluded_paths):
            continue

        file_paths.append(path)

    total_files = len(file_paths)

    # Second pass: collect metadata
    for idx, path in enumerate(file_paths):
        try:
            stat = path.stat()
            file_hash = None

            if compute_hashes:
                file_hash = compute_file_hash(path)

            if extract_content:
                try:
                    # Extract content for AI analysis (Phase 5)
                    # Currently testing extraction capability
                    extract_text(path)
                except Exception:
                    # Extraction errors are not fatal
                    pass

            results.append(
                FileMetadata(
                    name=path.name,
                    path=str(path),
                    extension=path.suffix.lower(),
                    size=stat.st_size,
                    modified=stat.st_mtime,
                    relative_path=str(path.relative_to(folder)),
                    sha256=file_hash,
                )
            )

            if progress_callback:
                progress_callback(idx + 1, total_files)

        except OSError:
            # Skip files that cannot be accessed
            continue

    return results


def scan_and_persist(
    folder: Path,
    excluded_paths: list[str] | None = None,
    compute_hashes: bool = True,
    extract_content: bool = False,
    progress_callback: Callable[[int, int], None] | None = None,
    recursive: bool = True,
) -> list[FileMetadata]:
    """
    Scan a folder and persist results to the database.

    Args:
        folder: Path to the folder to scan
        excluded_paths: List of path patterns to exclude
        compute_hashes: Whether to compute SHA-256 hashes
        extract_content: Whether to extract text content
        progress_callback: Optional callback for progress updates

    Returns:
        List of FileMetadata objects
    """
    files = scan_folder(
        folder, excluded_paths, compute_hashes, extract_content, progress_callback, recursive
    )

    # Persist to database
    repo = FileRepository()
    for file_data in files:
        repo.save_file(
            {
                "name": file_data.name,
                "relative_path": file_data.relative_path,
                "extension": file_data.extension,
                "size": file_data.size,
                "modified": file_data.modified,
                "sha256": file_data.sha256,
                "last_scanned_at": 0,  # Will be set by database
            }
        )

    return files
