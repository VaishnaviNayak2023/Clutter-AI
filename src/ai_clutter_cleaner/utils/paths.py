"""Path utility functions."""

from pathlib import Path


def resolve_path(path: str | Path) -> Path:
    """
    Resolve a path to an absolute path.

    Args:
        path: Path to resolve

    Returns:
        Resolved absolute Path
    """
    return Path(path).expanduser().resolve()


def is_path_safe(path: Path, root: Path) -> bool:
    """
    Check if a path is safely contained within a root directory.

    Args:
        path: Path to check
        root: Root directory

    Returns:
        True if path is safe, False otherwise
    """
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False
