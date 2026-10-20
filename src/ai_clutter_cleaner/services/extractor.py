"""Document text extraction service."""

from pathlib import Path

from src.ai_clutter_cleaner.exceptions import ExtractionError


def extract_text(path: Path) -> str:
    """
    Extract text from a supported document format.

    Args:
        path: Path to the document

    Returns:
        Extracted text content

    Raises:
        ExtractionError: If extraction fails
    """
    suffix = path.suffix.lower()

    # Plain text files
    if suffix in {".txt", ".md", ".py", ".csv", ".json"}:
        try:
            return path.read_text(encoding="utf-8", errors="replace")
        except OSError as e:
            raise ExtractionError(f"Failed to read {path}: {e}")

    # PDF files
    if suffix == ".pdf":
        try:
            from pypdf import PdfReader

            reader = PdfReader(str(path))
            if reader.is_encrypted:
                return ""

            return "\n".join(page.extract_text() or "" for page in reader.pages)
        except Exception as e:
            raise ExtractionError(f"Failed to extract PDF from {path}: {e}")

    # DOCX files
    if suffix == ".docx":
        try:
            from docx import Document

            document = Document(str(path))
            return "\n".join(paragraph.text for paragraph in document.paragraphs)
        except Exception as e:
            raise ExtractionError(f"Failed to extract DOCX from {path}: {e}")

    return ""
