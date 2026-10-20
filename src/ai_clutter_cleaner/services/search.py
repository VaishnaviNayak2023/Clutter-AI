"""Search service."""

from dataclasses import dataclass


@dataclass
class SearchFilter:
    """Filter criteria for file search."""

    query: str = ""
    extension: str | None = None
    category: str | None = None
    min_size_kb: float = 0
    max_size_kb: float | None = None
    search_content: bool = False
    exact_match: bool = False
    include_system_files: bool = False


def search_files(files: list, filters: SearchFilter) -> list:
    """
    Search and filter files based on criteria.

    Args:
        files: List of file metadata dictionaries
        filters: SearchFilter with search criteria

    Returns:
        Filtered list of files
    """
    results = []

    for file in files:
        if not filters.include_system_files:
            path_parts = file.get("path", "").replace("\\", "/").split("/")
            if any(
                part.startswith(".")
                or part.casefold() in {"system volume information", "$recycle.bin"}
                for part in path_parts
            ):
                continue

        # Query search (filename)
        if filters.query:
            query = filters.query.casefold()
            if filters.exact_match:
                name_match = query == file.get("name", "").casefold()
                path_match = query == file.get("path", "").casefold()
            else:
                name_match = query in file.get("name", "").casefold()
                path_match = query in file.get("path", "").casefold()
            content = str(file.get("content", "")).casefold()
            content_match = filters.search_content and (
                query == content if filters.exact_match else query in content
            )

            if not (name_match or path_match or content_match):
                continue

        # Extension filter
        if filters.extension:
            if file.get("extension") != filters.extension.lower():
                continue

        # Category filter
        if filters.category:
            if file.get("category") != filters.category:
                continue

        # Size filter
        size_kb = file.get("size", 0) / 1_000
        if size_kb < filters.min_size_kb:
            continue

        if filters.max_size_kb is not None and size_kb > filters.max_size_kb:
            continue

        results.append(file)

    return results


def search_by_extension(files: list, extension: str) -> list:
    """
    Filter files by extension.

    Args:
        files: List of file metadata
        extension: File extension to filter by (e.g., ".pdf")

    Returns:
        Filtered list of files
    """
    return [f for f in files if f.get("extension") == extension.lower()]


def search_by_category(files: list, category: str) -> list:
    """
    Filter files by category.

    Args:
        files: List of file metadata with category field
        category: Category to filter by

    Returns:
        Filtered list of files
    """
    return [f for f in files if f.get("category") == category]


def search_by_size(files: list, min_kb: float = 0, max_kb: float | None = None) -> list:
    """
    Filter files by size.

    Args:
        files: List of file metadata
        min_kb: Minimum size in KB
        max_kb: Maximum size in KB (None for no limit)

    Returns:
        Filtered list of files
    """
    results = []
    for f in files:
        size_kb = f.get("size", 0) / 1_000
        if size_kb >= min_kb:
            if max_kb is None or size_kb <= max_kb:
                results.append(f)
    return results
