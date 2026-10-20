"""Database repositories for data access."""


from src.ai_clutter_cleaner.database.connection import get_db_connection


class FileRepository:
    """Repository for file metadata operations."""

    def __init__(self, db_path=None):
        self.db_path = db_path

    def save_file(self, file_data: dict) -> int:
        """Save file metadata and return the file ID."""
        conn = get_db_connection(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO files (
                    relative_path, filename, extension, size_bytes,
                    modified_at, sha256, content_fingerprint, extraction_status, last_scanned_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    file_data.get("relative_path"),
                    file_data["name"],
                    file_data["extension"],
                    file_data["size"],
                    file_data["modified"],
                    file_data.get("sha256"),
                    file_data.get("content_fingerprint"),
                    file_data.get("extraction_status", "pending"),
                    file_data.get("last_scanned_at"),
                ),
            )
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    def get_file_by_path(self, path: str) -> dict | None:
        """Get file metadata by path."""
        conn = get_db_connection(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM files WHERE relative_path = ?", (path,))
            row = cursor.fetchone()
            return dict(row) if row else None
        finally:
            conn.close()

    def get_files_by_hash(self, sha256: str) -> list[dict]:
        """Get all files with a specific SHA-256 hash."""
        conn = get_db_connection(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM files WHERE sha256 = ?", (sha256,))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()
