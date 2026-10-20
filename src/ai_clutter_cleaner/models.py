"""Data models for the application."""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class FileMetadata:
    """Metadata for a scanned file."""

    name: str
    path: str
    extension: str
    size: int
    modified: float
    relative_path: str | None = None
    sha256: str | None = None


@dataclass
class ScanResult:
    """Result of a folder scan."""

    files: list[FileMetadata]
    total_size: int
    scan_time: datetime
    root_path: str
    errors: list[str]


@dataclass
class CategoryPrediction:
    """AI category prediction for a file."""

    category: str
    confidence: float
    reason: str
    model_version: str


@dataclass
class SimilarityMatch:
    """Semantic similarity between two documents."""

    file_id_a: int
    file_id_b: int
    similarity_score: float
    comparison_method: str
