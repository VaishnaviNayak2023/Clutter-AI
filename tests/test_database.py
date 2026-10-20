"""Tests for the database module."""

import tempfile
from pathlib import Path

from src.ai_clutter_cleaner.database import get_db_connection, init_database


def test_database_initialization():
    """Test that the database can be initialized."""
    with tempfile.TemporaryDirectory() as temp_dir:
        db_path = Path(temp_dir) / "test.db"
        init_database(db_path)

        # Verify database was created
        assert db_path.exists()

        # Verify we can connect
        conn = get_db_connection(db_path)
        assert conn is not None
        conn.close()


def test_database_schema():
    """Test that the database schema is correct."""
    with tempfile.TemporaryDirectory() as temp_dir:
        db_path = Path(temp_dir) / "test.db"
        init_database(db_path)

        conn = get_db_connection(db_path)
        cursor = conn.cursor()

        # Check that tables exist
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        )
        tables = [row[0] for row in cursor.fetchall()]

        expected_tables = [
            "files",
            "predictions",
            "embeddings",
            "similarity_matches",
            "scan_jobs",
            "file_actions",
            "settings",
        ]

        for table in expected_tables:
            assert table in tables

        conn.close()
