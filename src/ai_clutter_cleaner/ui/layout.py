"""Shared application shell and page navigation."""

import shutil

import streamlit as st

PAGE_LABELS = {
    "Dashboard": "Overview",
    "Scan_Files": "Scan Files",
    "AI_Organization": "AI Organization",
    "Duplicate_Finder": "Duplicate Finder",
    "Search_Explorer": "Search Explorer",
    "History": "History & Activity",
    "Reports": "Reports",
    "Settings": "Settings",
}

NAVIGATION = {
    "WORKSPACE": [
        ("Overview", "Dashboard", ":material/dashboard:"),
        ("Scan Files", "Scan_Files", ":material/folder_open:"),
        ("AI Organization", "AI_Organization", ":material/auto_awesome:"),
        ("Duplicate Finder", "Duplicate_Finder", ":material/content_copy:"),
    ],
    "EXPLORE": [
        ("Search Explorer", "Search_Explorer", ":material/search:"),
        ("History & Activity", "History", ":material/history:"),
        ("Reports", "Reports", ":material/description:"),
    ],
    "PREFERENCES": [
        ("Settings", "Settings", ":material/settings:"),
    ],
}


def init_page_state() -> None:
    """Initialize the state used by the single custom navigation system."""
    requested_page = st.query_params.get("view")
    if requested_page in PAGE_LABELS:
        st.session_state["current_page"] = requested_page
    else:
        st.session_state.setdefault("current_page", "Dashboard")


def navigate_to_page(page_name: str) -> None:
    """Navigate to a registered application page."""
    if page_name not in PAGE_LABELS:
        raise ValueError(f"Unknown page: {page_name}")
    st.session_state["current_page"] = page_name
    st.query_params["view"] = page_name


def render_sidebar() -> None:
    """Render branding, one navigation menu, and local workspace status."""
    with st.sidebar:
        st.markdown(
            """
            <div class="brand">
                <span class="brand-mark" aria-hidden="true">
                    <svg viewBox="0 0 24 24" aria-hidden="true">
                        <path d="M3 5.5A2.5 2.5 0 0 1 5.5 3H10l2.2 2.2H19A2.5 2.5 0 0 1 21.5 7.7v10.8A2.5 2.5 0 0 1 19 21H5a2.5 2.5 0 0 1-2.5-2.5v-13Z"/>
                    </svg>
                </span>
                <div>
                    <div class="brand-name">ClutterAI</div>
                    <div class="brand-subtitle">Intelligent File Management</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        active_page = st.session_state.get("current_page", "Dashboard")
        for group, items in NAVIGATION.items():
            st.markdown(f'<div class="nav-group-label">{group}</div>', unsafe_allow_html=True)
            for label, page, icon in items:
                if st.button(
                    label,
                    key=f"nav_{page}",
                    icon=icon,
                    type="primary" if active_page == page else "secondary",
                    width="stretch",
                ):
                    navigate_to_page(page)

        try:
            disk = shutil.disk_usage(st.session_state.get("last_scanned_folder") or ".")
        except OSError:
            disk = shutil.disk_usage(".")
        disk_used_gb = disk.used / 1_000_000_000
        disk_total_gb = disk.total / 1_000_000_000
        disk_percent = disk.used / disk.total * 100 if disk.total else 0
        st.markdown(
            f"""
            <div class="workspace-status">
                <div class="workspace-status-title">
                    <span class="workspace-database" aria-hidden="true">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7">
                            <ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v6c0 1.7 3.6 3 8 3s8-1.3 8-3V5M4 11v6c0 1.7 3.6 3 8 3s8-1.3 8-3v-6"/>
                        </svg>
                    </span>
                    <span>Local Workspace<br><small><span class="status-dot"></span> Ready</small></span>
                </div>
                <div class="workspace-status-meta">{disk_used_gb:.1f} GB of {disk_total_gb:.0f} GB used</div>
                <div class="workspace-meter"><span style="width:{disk_percent:.1f}%"></span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_global_header() -> None:
    """Render functional global search and shortcuts shared by every page."""
    st.session_state.setdefault(
        "global_search_input", st.session_state.get("global_search_query", "")
    )
    with st.container(key="app-global-header"):
        search_col, scan_col, refresh_col, settings_col, _spacer = st.columns(
            [4, 1.25, 0.45, 0.8, 3.5]
        )
        with search_col:
            st.text_input(
                "Search indexed files",
                placeholder="Search files, folders, or content...",
                label_visibility="collapsed",
                icon=":material/search:",
                key="global_search_input",
                on_change=_submit_global_search,
            )

        with scan_col:
            if st.button(
                "Open Scan Folder", icon=":material/folder_open:", key="header_scan",
                width="stretch",
            ):
                navigate_to_page("Scan_Files")
        with refresh_col:
            if st.button(
                "⟳", key="header_refresh", help="Refresh this view", width="stretch"
            ):
                st.rerun()
        with settings_col:
            if st.button(
                "Settings", icon=":material/settings:", key="header_settings",
                width="stretch",
            ):
                navigate_to_page("Settings")


def _submit_global_search() -> None:
    """Carry the global search query into Search Explorer."""
    query = st.session_state.get("global_search_input", "")
    st.session_state["global_search_query"] = query
    st.session_state["search_query"] = query
    st.session_state["search_query_input"] = query
    navigate_to_page("Search_Explorer")


def format_size(size_bytes: int) -> str:
    """Format a byte count with an appropriate binary unit."""
    if size_bytes >= 1_000_000_000:
        return f"{size_bytes / 1_000_000_000:.2f} GB"
    if size_bytes >= 1_000_000:
        return f"{size_bytes / 1_000_000:.1f} MB"
    if size_bytes >= 1_000:
        return f"{size_bytes / 1_000:.1f} KB"
    return f"{size_bytes:,} B"
