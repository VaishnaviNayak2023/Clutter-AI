"""Small UI helpers for session activity and persisted preferences."""

import json
from datetime import datetime
from typing import Any

import streamlit as st

from src.ai_clutter_cleaner.database.connection import get_db_connection

DEFAULT_EXCLUDED_PATHS = ".git\nnode_modules\n__pycache__\n.venv\nvenv\n.env"


def get_preference(key: str, default: Any) -> Any:
    """Load one JSON-encoded preference from the existing settings table."""
    connection = get_db_connection()
    try:
        row = connection.execute("SELECT value FROM settings WHERE key = ?", (key,)).fetchone()
    finally:
        connection.close()

    if row is None:
        return default
    try:
        return json.loads(row["value"])
    except (TypeError, json.JSONDecodeError):
        return default


def save_preferences(values: dict[str, Any]) -> None:
    """Persist preference values using the existing settings table."""
    connection = get_db_connection()
    try:
        connection.executemany(
            """
            INSERT INTO settings (key, value, updated_at)
            VALUES (?, ?, ?)
            ON CONFLICT(key) DO UPDATE SET
                value = excluded.value,
                updated_at = excluded.updated_at
            """,
            [
                (key, json.dumps(value), datetime.now().timestamp())
                for key, value in values.items()
            ],
        )
        connection.commit()
    finally:
        connection.close()


def record_session_activity(action: str, details: str, status: str = "Completed") -> None:
    """Append an activity item that lasts for the current Streamlit session."""
    activities = st.session_state.setdefault("activity_log", [])
    activities.insert(
        0,
        {
            "Action": action,
            "Details": details,
            "Time": datetime.now().astimezone().strftime("%b %d, %Y %I:%M %p"),
            "Status": status,
        },
    )
    del activities[50:]
