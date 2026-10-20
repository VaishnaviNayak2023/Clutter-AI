"""Persisted application preferences and workspace information."""

import streamlit as st

from src.ai_clutter_cleaner.config import BASE_DIR, DEFAULT_DB_NAME, SUPPORTED_EXTENSIONS
from src.ai_clutter_cleaner.database.connection import get_db_connection
from src.ai_clutter_cleaner.ui import (
    render_global_header,
    render_page_header,
    render_section_header,
)
from src.ai_clutter_cleaner.ui.data import (
    DEFAULT_EXCLUDED_PATHS,
    get_preference,
    save_preferences,
)


def render_settings() -> None:
    """Render only settings that are connected to existing behavior."""
    render_global_header()
    render_page_header(
        title="Settings",
        subtitle="Configure scan defaults and duplicate analysis preferences.",
        breadcrumb=["Preferences", "Settings"],
    )

    render_section_header("Scanning defaults", icon="scan")
    with st.form("application_settings", border=True):
        hash_col, persist_col, extract_col = st.columns(3)
        with hash_col:
            compute_hashes = st.checkbox(
                "Compute SHA-256 hashes",
                value=get_preference("scan.compute_hashes", True),
                help="Used for exact duplicate detection.",
            )
        with persist_col:
            persist_to_db = st.checkbox(
                "Save scan metadata",
                value=get_preference("scan.persist_to_db", True),
                help="Save file metadata to the local SQLite database.",
            )
        with extract_col:
            extract_content = st.checkbox(
                "Extract text during scan",
                value=get_preference("scan.extract_content", False),
                help="Run document text extraction while scanning.",
            )
        excluded_paths = st.text_area(
            "Default excluded path fragments",
            value=get_preference("scan.excluded_paths", DEFAULT_EXCLUDED_PATHS),
            help="One path fragment per line. These are passed to the existing scanner.",
            height=110,
        )

        render_section_header("Duplicate detection", icon="duplicate")
        similarity_threshold = st.slider(
            "Semantic similarity threshold",
            min_value=0.50,
            max_value=0.99,
            value=get_preference("duplicates.similarity_threshold", 0.75),
            step=0.01,
            help="Minimum model score for a pair to appear as semantically similar.",
        )

        save_col, reset_col = st.columns(2)
        with save_col:
            save = st.form_submit_button(
                "Save settings", type="primary", width="stretch"
            )
        with reset_col:
            reset = st.form_submit_button("Reset defaults", width="stretch")

    if reset:
        save_preferences(
            {
                "scan.compute_hashes": True,
                "scan.persist_to_db": True,
                "scan.extract_content": False,
                "scan.excluded_paths": DEFAULT_EXCLUDED_PATHS,
                "duplicates.similarity_threshold": 0.75,
            }
        )
        st.success("Settings restored to defaults.")
        st.rerun()
    elif save:
        save_preferences(
            {
                "scan.compute_hashes": compute_hashes,
                "scan.persist_to_db": persist_to_db,
                "scan.extract_content": extract_content,
                "scan.excluded_paths": excluded_paths,
                "duplicates.similarity_threshold": similarity_threshold,
            }
        )
        st.success("Settings saved to the local SQLite database.")

    render_section_header("Storage and privacy", icon="shield_check")
    connection = get_db_connection()
    try:
        indexed_count = connection.execute("SELECT COUNT(*) FROM files").fetchone()[0]
    finally:
        connection.close()

    info_col, privacy_col = st.columns(2)
    with info_col:
        with st.container(border=True):
            st.markdown("**Local database**")
            st.caption(str(BASE_DIR / DEFAULT_DB_NAME))
            st.caption(f"{indexed_count:,} file metadata records stored")
    with privacy_col:
        with st.container(border=True):
            st.markdown("**Processing**")
            st.caption(
                "Scanning and document extraction use files at the selected local paths. "
                "Semantic analysis may download its configured model on first use; the model "
                "then processes extracted text in the local application."
            )

    render_section_header("Supported file extensions", icon="files")
    st.caption(", ".join(sorted(SUPPORTED_EXTENSIONS)))
