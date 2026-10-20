"""Database connection and initialization."""

import sqlite3
from pathlib import Path

from src.ai_clutter_cleaner.config import BASE_DIR, DEFAULT_DB_NAME
from src.ai_clutter_cleaner.exceptions import DatabaseError


def get_db_connection(db_path: Path | None = None) -> sqlite3.Connection:
    """Get a database connection."""
    if db_path is None:
        db_path = BASE_DIR / DEFAULT_DB_NAME

    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        raise DatabaseError(f"Failed to connect to database: {e}")


def init_database(db_path: Path | None = None) -> None:
    """Initialize the database schema."""
    conn = get_db_connection(db_path)
    cursor = conn.cursor()

    schema = """
    CREATE TABLE IF NOT EXISTS files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        root_id INTEGER,
        relative_path TEXT NOT NULL,
        filename TEXT NOT NULL,
        extension TEXT NOT NULL,
        size_bytes INTEGER NOT NULL,
        modified_at REAL NOT NULL,
        sha256 TEXT,
        content_fingerprint TEXT,
        extraction_status TEXT DEFAULT 'pending',
        last_scanned_at REAL
    );

    CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_id INTEGER NOT NULL,
        category TEXT NOT NULL,
        confidence REAL NOT NULL,
        reason TEXT,
        model_version TEXT,
        created_at REAL NOT NULL,
        FOREIGN KEY (file_id) REFERENCES files(id)
    );

    CREATE TABLE IF NOT EXISTS embeddings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_id INTEGER NOT NULL,
        model_name TEXT NOT NULL,
        model_version TEXT,
        content_fingerprint TEXT,
        vector_storage_reference TEXT,
        created_at REAL NOT NULL,
        FOREIGN KEY (file_id) REFERENCES files(id)
    );

    CREATE TABLE IF NOT EXISTS similarity_matches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_id_a INTEGER NOT NULL,
        file_id_b INTEGER NOT NULL,
        similarity_score REAL NOT NULL,
        comparison_method TEXT NOT NULL,
        model_version TEXT,
        created_at REAL NOT NULL,
        FOREIGN KEY (file_id_a) REFERENCES files(id),
        FOREIGN KEY (file_id_b) REFERENCES files(id)
    );

    CREATE TABLE IF NOT EXISTS scan_jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        root_path TEXT NOT NULL,
        status TEXT NOT NULL,
        started_at REAL NOT NULL,
        completed_at REAL,
        scanned_count INTEGER DEFAULT 0,
        error_count INTEGER DEFAULT 0
    );

    CREATE TABLE IF NOT EXISTS file_actions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        operation_id TEXT NOT NULL,
        action_type TEXT NOT NULL,
        source_path TEXT NOT NULL,
        destination_path TEXT,
        status TEXT NOT NULL,
        source_fingerprint TEXT,
        error_message TEXT,
        created_at REAL NOT NULL,
        completed_at REAL,
        undone_at REAL
    );

    CREATE TABLE IF NOT EXISTS settings (
        key TEXT PRIMARY KEY,
        value TEXT NOT NULL,
        updated_at REAL NOT NULL
    );

    CREATE INDEX IF NOT EXISTS idx_files_sha256 ON files(sha256);
    CREATE INDEX IF NOT EXISTS idx_files_extension ON files(extension);
    CREATE INDEX IF NOT EXISTS idx_predictions_file_id ON predictions(file_id);
    CREATE INDEX IF NOT EXISTS idx_similarity_score ON similarity_matches(similarity_score);
    """

    try:
        cursor.executescript(schema)
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        raise DatabaseError(f"Failed to initialize database: {e}")
    finally:
        conn.close()
