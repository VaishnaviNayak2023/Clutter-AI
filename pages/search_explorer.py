"""Search and inspect files in the current scan."""

import mimetypes
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st

from src.ai_clutter_cleaner.exceptions import ExtractionError
from src.ai_clutter_cleaner.services.extractor import extract_text
from src.ai_clutter_cleaner.services.search import SearchFilter, search_files
from src.ai_clutter_cleaner.ui import (
    navigate_to_page,
    render_empty_state,
    render_global_header,
    render_page_header,
    render_section_header,
)
from src.ai_clutter_cleaner.ui.layout import format_size


def render_search_explorer() -> None:
    """Render searchable scan metadata and a live details panel."""
    render_global_header()
    render_page_header(
        title="Search Explorer",
        subtitle="Find files by name, content, extension, category, or size.",
        breadcrumb=["Workspace", "Search Explorer"],
        icon="search",
    )

    scanned = st.session_state.get("scan_results") or []
    if not scanned:
        with st.container(border=True):
            with st.form("empty_file_search_form", border=False):
                query_col, search_col = st.columns([5, 1])
                with query_col:
                    query = st.text_input(
                        "Search query", placeholder="Search by name, path, or file content...",
                        key="empty_search_query",
                    )
                with search_col:
                    submitted = st.form_submit_button(
                        "Search", type="primary", icon=":material/search:", width="stretch"
                    )
                filter_cols = st.columns(4)
                for column, label, options in zip(
                    filter_cols,
                    ["File Type", "Category", "Size Range", "Modified Date"],
                    [["All Types"], ["All Categories"], ["All Sizes"], ["Any Time"]],
                    strict=True,
                ):
                    with column:
                        st.selectbox(label, options, disabled=True, key=f"empty_filter_{label}")
                content_col, exact_col, system_col = st.columns(3)
                with content_col:
                    st.checkbox("Search in file content", value=True, disabled=True)
                with exact_col:
                    st.checkbox("Exact match only", disabled=True)
                with system_col:
                    st.checkbox("Include system files", disabled=True)
        if submitted:
            st.session_state["global_search_query"] = query
        results_col, details_col = st.columns([3.15, 1])
        with results_col, st.container(border=True):
            render_section_header("Search Results (0)", icon="files")
            st.caption("Results will appear after you scan a folder.")
            st.dataframe(
                pd.DataFrame(columns=["Name", "Extension", "Size", "Category", "Modified", "Path", "Actions"]),
                width="stretch", hide_index=True,
            )
            if st.button("Scan a folder to populate results", type="primary", key="search_go_to_scan"):
                navigate_to_page("Scan_Files")
        with details_col, st.container(border=True):
            render_section_header("File details", icon="file_text")
            st.markdown('<div class="file-preview-placeholder"></div>', unsafe_allow_html=True)
            st.caption("Select a search result to see its preview and metadata.")
            st.divider()
            st.markdown("**Related Files**")
            st.caption("Related files will appear here.")
        return

    classification = st.session_state.get("classification_results") or []
    category_by_path = {row["path"]: row["category"] for row in classification}
    files = [
        {
            "name": file.name,
            "path": file.path,
            "relative_path": file.relative_path or file.path,
            "extension": file.extension,
            "size": file.size,
            "modified": file.modified,
            "category": category_by_path.get(file.relative_path or file.path, "Unclassified"),
            "sha256": file.sha256,
        }
        for file in scanned
    ]
    extensions = sorted({file["extension"] for file in files if file["extension"]})
    categories = sorted({file["category"] for file in files})
    max_size_kb = max(file["size"] for file in files) / 1_000
    dates = [datetime.fromtimestamp(file["modified"]).date() for file in files]
    scan_timestamp = st.session_state.get("scan_timestamp")
    scan_key = scan_timestamp.isoformat() if scan_timestamp else None
    if st.session_state.get("_search_scan_key") != scan_key:
        for key in (
            "search_query_input",
            "search_extension",
            "search_category",
            "search_size_bucket",
            "search_modified_filter",
        ):
            st.session_state.pop(key, None)
        st.session_state["_search_scan_key"] = scan_key
    st.session_state.setdefault(
        "search_query_input",
        st.session_state.get("global_search_query", st.session_state.get("search_query", "")),
    )

    with st.container(border=True):
        render_section_header("Search and filters", icon="search")
        with st.form("file_search_form", border=False):
            query_col, search_col = st.columns([5, 1])
            with query_col:
                query = st.text_input(
                    "Search query",
                    placeholder="Search by name, path, or file content...",
                    key="search_query_input",
                )
            with search_col:
                st.markdown("<div style='height: 1.7rem'></div>", unsafe_allow_html=True)
                submitted = st.form_submit_button(
                    "Search", type="primary", icon=":material/search:", width="stretch"
                )

            filter_cols = st.columns(4)
            with filter_cols[0]:
                extension = st.selectbox(
                    "File Type", ["All types", *extensions], key="search_extension"
                )
            with filter_cols[1]:
                category = st.selectbox(
                    "Category", ["All categories", *categories], key="search_category"
                )
            with filter_cols[2]:
                size_bucket = st.selectbox(
                    "Size Range",
                    ["All Sizes", "Under 1 MB", "1 - 10 MB", "10 - 100 MB", "Over 100 MB"],
                    key="search_size_bucket",
                )
            with filter_cols[3]:
                modified_filter = st.selectbox(
                    "Modified Date",
                    ["Any Time", "Last 7 days", "Last 30 days", "Last year"],
                    key="search_modified_filter",
                )
            exact_match, search_content, include_system = st.columns(3)
            with exact_match:
                exact_only = st.checkbox("Exact match only")
            with search_content:
                content_search = st.checkbox(
                    "Search in file content",
                    value=True,
                    help="Reads supported files locally when this option is enabled.",
                )
            with include_system:
                include_hidden = st.checkbox("Include hidden/system files")

    st.button(
        "Clear filters",
        key="search_clear_filters",
        on_click=_reset_search_filters,
    )

    if submitted:
        st.session_state["search_query"] = query

    if content_search and query:
        extraction_errors = []
        with st.spinner("Searching supported file contents..."):
            for item in files:
                try:
                    item["content"] = extract_text(Path(item["path"]))
                except ExtractionError as error:
                    extraction_errors.append(item["name"])
                    st.warning(f"Could not search content in {item['name']}: {error}")
        if not extraction_errors:
            st.caption("Content search ran against the supported files in this scan.")

    size_ranges = {
        "All Sizes": (0.0, max(max_size_kb, 1.0)),
        "Under 1 MB": (0.0, 1_024.0),
        "1 - 10 MB": (1_024.0, 10_240.0),
        "10 - 100 MB": (10_240.0, 102_400.0),
        "Over 100 MB": (102_400.0, max(max_size_kb, 102_400.0)),
    }
    min_size, max_size = size_ranges[size_bucket]
    filters = SearchFilter(
        query=query,
        extension=extension if extension != "All types" else None,
        category=category if category != "All categories" else None,
        min_size_kb=min_size,
        max_size_kb=max_size,
        search_content=content_search,
        exact_match=exact_only,
        include_system_files=include_hidden,
    )
    results = search_files(files, filters)
    modified_days = {"Last 7 days": 7, "Last 30 days": 30, "Last year": 365}.get(
        modified_filter
    )
    if modified_days is not None:
        end_date = datetime.now().date()
        start_date = end_date - pd.Timedelta(days=modified_days).to_pytimedelta()
        results = [
            item
            for item in results
            if start_date <= datetime.fromtimestamp(item["modified"]).date() <= end_date
        ]

    with st.container(border=True):
        result_col, detail_col = st.columns([3.15, 1])
        with result_col:
            render_section_header("Search results", icon="files")
            st.caption(f"{len(results):,} matching files from {len(files):,} scanned")
            if not results:
                render_empty_state(
                    title="No matching files",
                    message="Try a broader search or clear one or more filters.",
                    icon="search",
                )
                return

            controls = st.columns([2, 1])
            with controls[1]:
                sort_by = st.selectbox(
                    "Sort results",
                    ["Relevance", "Name", "Largest first", "Recently modified"],
                    label_visibility="collapsed",
                    key="search_sort",
                )
            if sort_by == "Name":
                results.sort(key=lambda item: item["name"].casefold())
            elif sort_by == "Largest first":
                results.sort(key=lambda item: item["size"], reverse=True)
            elif sort_by == "Recently modified":
                results.sort(key=lambda item: item["modified"], reverse=True)

            page_size = 10
            page_count = max((len(results) + page_size - 1) // page_size, 1)
            if st.session_state.get("search_page", 1) > page_count:
                st.session_state["search_page"] = page_count
            page_number = st.number_input(
                f"Page (1-{page_count})", min_value=1, max_value=page_count,
                value=min(st.session_state.get("search_page", 1), page_count),
                step=1, key="search_page", label_visibility="collapsed",
            )
            start = (int(page_number) - 1) * page_size
            page_results = results[start : start + page_size]
            result_table = pd.DataFrame(
                [
                    {
                        "Name": item["name"],
                        "Extension": item["extension"] or "Unknown",
                        "Size": format_size(item["size"]),
                        "Category": item["category"],
                        "Modified": datetime.fromtimestamp(item["modified"])
                        .astimezone()
                        .strftime("%b %d, %Y %I:%M %p"),
                        "Path": item["relative_path"],
                    }
                    for item in page_results
                ]
            )
            st.dataframe(result_table, width="stretch", hide_index=True)

        with detail_col:
            render_section_header("File details", icon="file_text")
            current_paths = [item["path"] for item in page_results]
            previous = st.session_state.get("search_selected_path")
            selected_path = previous if previous in current_paths else current_paths[0]
            selected_path = st.selectbox(
                "Selected file",
                options=current_paths,
                index=current_paths.index(selected_path),
                format_func=lambda path: next(
                    item["name"] for item in page_results if item["path"] == path
                ),
                key="search_selected_path",
            )
            selected = next(item for item in results if item["path"] == selected_path)
            st.markdown(f"**{selected['name']}**")
            st.caption(f"{selected['extension'] or 'Unknown'} · {format_size(selected['size'])}")
            st.caption(selected["relative_path"])
            suffix = Path(selected["path"]).suffix.lower()
            if suffix in {".txt", ".md", ".py", ".csv", ".json", ".docx", ".pdf"}:
                try:
                    preview = extract_text(Path(selected["path"]))
                except ExtractionError as error:
                    st.warning(f"Preview unavailable: {error}")
                else:
                    if preview.strip():
                        st.code(preview[:2_500], language="text")
                    else:
                        st.info("No text preview is available for this file.")
            else:
                st.info(f"Preview is not available for {suffix or 'this file type'}.")

            try:
                file_bytes = Path(selected["path"]).read_bytes()
            except OSError as error:
                st.error(f"File cannot be opened from this application: {error}")
            else:
                mime_type = mimetypes.guess_type(selected["name"])[0] or "application/octet-stream"
                st.download_button(
                    "Open File",
                    data=file_bytes,
                    file_name=selected["name"],
                    mime=mime_type,
                    help="Downloads a copy through the browser; it does not launch a local application.",
                    width="stretch",
                )

            with st.expander("View Metadata"):
                details = {
                    "Category": selected["category"],
                    "Extension": selected["extension"] or "Unknown",
                    "Size": format_size(selected["size"]),
                    "Modified": datetime.fromtimestamp(selected["modified"])
                    .astimezone()
                    .strftime("%b %d, %Y %I:%M %p"),
                    "Path": selected["path"],
                    "Content": "Extracted" if selected.get("content") else "Not extracted",
                    "SHA-256": selected["sha256"] or "Not computed",
                }
                for label, value in details.items():
                    st.caption(f"**{label}:** {value}")

            related = [
                item
                for item in results
                if item["path"] != selected["path"]
                and (
                    item["category"] == selected["category"]
                    or item["extension"] == selected["extension"]
                )
            ][:3]
            if related:
                st.markdown("**Related files**")
                for index, item in enumerate(related):
                    st.caption(f"{item['name']} · {format_size(item['size'])}")
                    if st.button(
                        f"View {item['name']}",
                        key=f"related_file_{index}",
                        width="stretch",
                    ):
                        st.session_state["search_selected_path"] = item["path"]
                        st.rerun()


def _reset_search_filters() -> None:
    st.session_state["global_search_query"] = ""
    st.session_state["search_query"] = ""
    for key in (
        "search_query_input",
        "search_extension",
        "search_category",
        "search_size_bucket",
        "search_modified_filter",
    ):
        st.session_state.pop(key, None)
