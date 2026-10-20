"""Custom exceptions for the application."""


class InvalidDirectoryError(Exception):
    """Raised when the specified directory is invalid or inaccessible."""

    pass


class ExtractionError(Exception):
    """Raised when document text extraction fails."""

    pass


class ModelUnavailableError(Exception):
    """Raised when the AI model is not available."""

    pass


class DatabaseError(Exception):
    """Raised when database operations fail."""

    pass


class DestinationConflictError(Exception):
    """Raised when a destination file already exists."""

    pass


class UnauthorizedPathError(Exception):
    """Raised when a path is outside the authorized root."""

    pass


class FileChangedError(Exception):
    """Raised when a file has changed since scanning."""

    pass
