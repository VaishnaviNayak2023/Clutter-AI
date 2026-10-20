"""Tests for the search service."""

from src.ai_clutter_cleaner.services.search import (
    SearchFilter,
    search_by_category,
    search_by_extension,
    search_by_size,
    search_files,
)


def test_search_files_by_query():
    """Test searching files by query."""
    files = [
        {"name": "document1.txt", "path": "/docs/document1.txt", "extension": ".txt"},
        {"name": "document2.pdf", "path": "/docs/document2.pdf", "extension": ".pdf"},
    ]

    filters = SearchFilter(query="document")
    results = search_files(files, filters)

    assert len(results) == 2


def test_search_files_by_extension():
    """Test searching files by extension."""
    files = [
        {"name": "document1.txt", "path": "/docs/document1.txt", "extension": ".txt"},
        {"name": "document2.pdf", "path": "/docs/document2.pdf", "extension": ".pdf"},
    ]

    filters = SearchFilter(extension=".txt")
    results = search_files(files, filters)

    assert len(results) == 1
    assert results[0]["extension"] == ".txt"


def test_search_files_by_category():
    """Test searching files by category."""
    files = [
        {"name": "doc1.txt", "extension": ".txt", "category": "Work"},
        {"name": "doc2.txt", "extension": ".txt", "category": "Personal"},
    ]

    filters = SearchFilter(category="Work")
    results = search_files(files, filters)

    assert len(results) == 1
    assert results[0]["category"] == "Work"


def test_search_by_extension():
    """Test the search_by_extension helper."""
    files = [
        {"name": "file1.txt", "extension": ".txt"},
        {"name": "file2.pdf", "extension": ".pdf"},
    ]

    results = search_by_extension(files, ".txt")

    assert len(results) == 1
    assert results[0]["extension"] == ".txt"


def test_search_by_category():
    """Test the search_by_category helper."""
    files = [
        {"name": "file1", "category": "Work"},
        {"name": "file2", "category": "Personal"},
    ]

    results = search_by_category(files, "Work")

    assert len(results) == 1
    assert results[0]["category"] == "Work"


def test_search_by_size():
    """Test the search_by_size helper."""
    files = [
        {"name": "small", "size": 1000},  # 1 KB
        {"name": "large", "size": 100000},  # 100 KB
    ]

    results = search_by_size(files, min_kb=50)

    assert len(results) == 1
    assert results[0]["name"] == "large"


def test_search_files_combined_filters():
    """Test searching with multiple filters."""
    files = [
        {
            "name": "work_doc.txt",
            "path": "/work/work_doc.txt",
            "extension": ".txt",
            "category": "Work",
            "size": 50000,
        },
        {
            "name": "personal_doc.txt",
            "path": "/personal/personal_doc.txt",
            "extension": ".txt",
            "category": "Personal",
            "size": 50000,
        },
    ]

    filters = SearchFilter(query="doc", extension=".txt", category="Work", min_size_kb=10)
    results = search_files(files, filters)

    assert len(results) == 1
    assert results[0]["category"] == "Work"


def test_search_files_exact_name_match():
    files = [
        {"name": "notes.txt", "path": "/docs/notes.txt"},
        {"name": "meeting-notes.txt", "path": "/docs/meeting-notes.txt"},
    ]

    results = search_files(files, SearchFilter(query="notes.txt", exact_match=True))

    assert [item["name"] for item in results] == ["notes.txt"]


def test_search_files_content_and_hidden_filters():
    files = [
        {
            "name": "report.txt",
            "path": "/docs/report.txt",
            "content": "quarterly revenue",
        },
        {
            "name": "draft.txt",
            "path": "/docs/.private/draft.txt",
            "content": "quarterly revenue",
        },
    ]

    results = search_files(
        files,
        SearchFilter(query="revenue", search_content=True),
    )

    assert [item["name"] for item in results] == ["report.txt"]
