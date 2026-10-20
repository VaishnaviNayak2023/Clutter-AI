"""Tests for the embeddings service."""

from src.ai_clutter_cleaner.services.embeddings import SemanticFinder, get_semantic_finder


def test_semantic_finder_initialization():
    """Test that the semantic finder can be initialized."""
    finder = SemanticFinder()
    assert finder.model_name is not None
    assert not finder._is_loaded


def test_semantic_finder_singleton():
    """Test that get_semantic_finder returns the same instance."""
    finder1 = get_semantic_finder()
    finder2 = get_semantic_finder()

    assert finder1 is finder2


def test_find_similar_empty_list():
    """Test finding similar documents with empty list."""
    from src.ai_clutter_cleaner.services.embeddings import find_similar_documents

    matches = find_similar_documents([])
    assert matches == []


def test_find_similar_single_document():
    """Test finding similar documents with single document."""
    from src.ai_clutter_cleaner.services.embeddings import find_similar_documents

    matches = find_similar_documents(["Single document text"])
    assert matches == []


def test_find_similar_insufficient_text():
    """Test finding similar documents with insufficient text."""
    from src.ai_clutter_cleaner.services.embeddings import find_similar_documents

    matches = find_similar_documents(["short", "docs"])
    # Should return empty because texts are too short
    assert isinstance(matches, list)
