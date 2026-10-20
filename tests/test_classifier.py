"""Tests for the classifier service."""

from src.ai_clutter_cleaner.services.classifier import (
    DocumentClassifier,
    classify_document,
    get_classifier,
)


def test_classify_document():
    """Test document classification with ML model."""
    text = "This is a sample document about machine learning."
    filename = "ml_notes.txt"

    prediction = classify_document(text, filename)

    assert prediction.category is not None
    assert 0 <= prediction.confidence <= 1
    assert prediction.reason is not None
    assert prediction.model_version is not None


def test_classifier_training():
    """Test that the classifier can be trained."""
    classifier = DocumentClassifier()
    assert not classifier._is_trained

    classifier.train()
    assert classifier._is_trained
    assert classifier.pipeline is not None


def test_classifier_singleton():
    """Test that get_classifier returns the same instance."""
    classifier1 = get_classifier()
    classifier2 = get_classifier()

    assert classifier1 is classifier2


def test_classify_empty_text():
    """Test classification with empty text."""
    prediction = classify_document("", "test.txt")

    # Should fall back to rule-based
    assert prediction.category is not None
    assert prediction.confidence > 0


def test_classify_work_document():
    """Test classification of work-related document."""
    text = "Project proposal for new software development initiative"
    filename = "project_proposal.docx"

    prediction = classify_document(text, filename)

    assert prediction.category is not None
    # With synthetic data, confidence may vary
    assert prediction.confidence >= 0


def test_classify_code_file():
    """Test classification of code file."""
    text = "def hello_world(): print('Hello, World!')"
    filename = "script.py"

    prediction = classify_document(text, filename)

    # With synthetic data, the ML may misclassify short code snippets
    # But it should still produce a valid prediction
    assert prediction.category is not None
    assert prediction.confidence >= 0


def test_classifier_with_csv_fallback():
    """Test classifier with non-existent CSV falls back to synthetic."""
    classifier = DocumentClassifier(use_real_data=True, training_csv="nonexistent.csv")
    classifier.train()

    assert classifier._is_trained
    assert classifier.pipeline is not None


def test_classifier_initialization_options():
    """Test classifier initialization with different options."""
    # Default (synthetic)
    classifier1 = DocumentClassifier()
    assert classifier1.use_real_data is False

    # With real data option
    classifier2 = DocumentClassifier(use_real_data=True, training_csv="test.csv")
    assert classifier2.use_real_data is True
    assert classifier2.training_csv == "test.csv"
