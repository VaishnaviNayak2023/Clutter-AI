"""Services package."""

from .classifier import classify_document, get_classifier
from .dataset_loader import DatasetLoader, load_training_data_from_csv
from .embeddings import find_similar_documents, get_semantic_finder
from .extractor import extract_text
from .hashing import compute_file_hash
from .history import get_history, record_action
from .organizer import FileOrganizer, propose_destination
from .scanner import scan_and_persist, scan_folder
from .search import (
    SearchFilter,
    search_by_category,
    search_by_extension,
    search_by_size,
    search_files,
)

__all__ = [
    "scan_folder",
    "scan_and_persist",
    "extract_text",
    "compute_file_hash",
    "classify_document",
    "get_classifier",
    "DatasetLoader",
    "load_training_data_from_csv",
    "find_similar_documents",
    "get_semantic_finder",
    "FileOrganizer",
    "propose_destination",
    "SearchFilter",
    "search_files",
    "search_by_extension",
    "search_by_category",
    "search_by_size",
    "get_history",
    "record_action",
]
