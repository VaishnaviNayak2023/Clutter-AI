"""Application configuration."""

from pathlib import Path

# Supported file extensions
SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".txt",
    ".md",
    ".docx",
    ".csv",
    ".json",
    ".py",
}

# Default categories
DEFAULT_CATEGORIES = [
    "Work and Projects",
    "Education and Notes",
    "Finance and Bills",
    "Career and Resumes",
    "Personal Documents",
    "Software and Code",
    "Images and Media",
    "Miscellaneous",
]

# Database configuration
DEFAULT_DB_NAME = "clutter_cleaner.db"

# Model configuration
DEFAULT_EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
SIMILARITY_THRESHOLD = 0.80

# Extraction limits
MAX_FILE_SIZE_MB = 50
MAX_PDF_PAGES = 100

# Paths
BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
