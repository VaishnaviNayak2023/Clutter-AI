"""Current-session history and activity."""

import pandas as pd
import streamlit as st

from src.ai_clutter_cleaner.ui import (
    render_empty_state,
    render_global_header,
    render_page_header,
    render_section_header,
)


def render_history() -> None:
    """Show activity recorded during this Streamlit session."""
    render_global_header()
    render_page_header(
        title="History & Activity",
        subtitle="Review scans and operations recorded in the current session.",
        breadcrumb=["Explore", "History & Activity"],
    )
    st.caption(
        "Activity is kept in session memory only. The current database history service "
        "does not yet persist action events across application restarts."
    )

    events = st.session_state.get("activity_log", [])
    if not events:
        render_empty_state(
            title="No activity recorded",
            message="Scan a folder, classify files, or run duplicate analysis to see activity here.",
            icon="clock",
        )
        return

    render_section_header("Activity log", icon="history")
    action_types = sorted({event["Action"] for event in events})
    filter_type = st.selectbox("Filter by action", ["All actions", *action_types])
    filtered = [
        event for event in events
        if filter_type == "All actions" or event["Action"] == filter_type
    ]
    st.metric("Activity entries", len(filtered))
    st.dataframe(
        pd.DataFrame(filtered),
        width="stretch",
        hide_index=True,
        column_config={
            "Action": st.column_config.TextColumn(width="medium"),
            "Details": st.column_config.TextColumn(width="large"),
            "Time": st.column_config.TextColumn(width="medium"),
            "Status": st.column_config.TextColumn(width="small"),
        },
    )

    scan_folder = st.session_state.get("last_scanned_folder")
    if scan_folder:
        with st.expander("Latest scan details"):
            st.text(f"Folder: {scan_folder}")
            st.text(f"Files: {st.session_state.get('total_files', 0):,}")
            st.text(f"Size: {st.session_state.get('total_size_mb', 0):.2f} MB")
