"""Folder scanning workspace."""

from datetime import datetime
from pathlib import Path
from time import time

import pandas as pd
import streamlit as st

from src.ai_clutter_cleaner.config import SUPPORTED_EXTENSIONS
from src.ai_clutter_cleaner.exceptions import DatabaseError, InvalidDirectoryError
from src.ai_clutter_cleaner.services import scan_and_persist, scan_folder
from src.ai_clutter_cleaner.ui import (
    render_empty_state,
    render_global_header,
    render_kpi_card,
    render_page_header,
    render_section_header,
)
from src.ai_clutter_cleaner.ui.data import (
    DEFAULT_EXCLUDED_PATHS,
    get_preference,
    record_session_activity,
)
from src.ai_clutter_cleaner.ui.layout import format_size


def render_scan_files() -> None:
    """Render scan configuration and current scan results."""
    render_global_header()
    render_page_header(
        title="Scan Files",
        subtitle=(
            "Index a folder to analyze file types, detect duplicates, "
            "and enable AI-powered organization."
        ),
        breadcrumb=["Workspace", "Scan Files"],
        icon="folder_open",
    )

    config_col, formats_col = st.columns([3.3, 1])
    with config_col:
        with st.container(border=True):
            render_section_header("Scan configuration", icon="scan")
            with st.form("scan_configuration", border=False):
                folder_path = st.text_input(
                    "Folder path",
                    value=st.session_state.get("last_scanned_folder", ""),
                    placeholder="Select a folder or enter a local path...",
                    help=(
                        "Enter a path accessible to the machine running ClutterAI. "
                        "A browser-only deployment cannot open arbitrary paths on your device."
                    ),
                )
                recursive_col, hash_col, persist_col, extract_col = st.columns(4)
                with recursive_col:
                    recursive = st.checkbox(
                        "Scan subdirectories",
                        value=True,
                        help="Include supported files in nested folders.",
                    )
                with hash_col:
                    compute_hashes = st.checkbox(
                        "Compute SHA-256 hashes",
                        value=get_preference("scan.compute_hashes", True),
                        help="Required for exact duplicate detection.",
                    )
                with persist_col:
                    persist_to_db = st.checkbox(
                        "Save results to database",
                        value=get_preference("scan.persist_to_db", True),
                        help="Save file metadata to the local SQLite database.",
                    )
                with extract_col:
                    extract_content = st.checkbox(
                        "Extract document content",
                        value=get_preference("scan.extract_content", False),
                        help="Run available text extractors while scanning.",
                    )
                excluded_input = st.text_area(
                    "Excluded directories (optional)",
                    value=get_preference("scan.excluded_paths", DEFAULT_EXCLUDED_PATHS),
                    placeholder="Enter directories or path fragments, one per line...",
                    help="Matching paths are skipped.",
                    height=80,
                )
                start_scan = st.form_submit_button(
                    "Start Scan", type="primary", icon=":material/play_arrow:"
                )
    with formats_col:
        with st.container(border=True):
            render_section_header("Supported file formats", icon="files")
            format_names = {
                ".txt": "Text files",
                ".md": "Markdown files",
                ".csv": "CSV files",
                ".json": "JSON files",
                ".py": "Python files",
                ".pdf": "PDF files",
                ".docx": "Word documents",
            }
            for extension in sorted(SUPPORTED_EXTENSIONS):
                st.markdown(f"**{extension[1:].upper()}**　{format_names.get(extension, 'Files')}")
            st.caption(
                "Scanning and metadata storage use the configured local application services."
            )

    if start_scan:
        if not folder_path.strip():
            st.warning("Enter a folder path to start scanning.")
        else:
            folder = Path(folder_path).expanduser()
            if not folder.is_dir():
                st.error("The folder does not exist or cannot be accessed.")
            else:
                progress_bar = st.progress(0, text="Preparing scan")
                status_line = st.empty()

                def update_progress(current: int, total: int) -> None:
                    progress_bar.progress(
                        current / total, text=f"Scanning {current:,} of {total:,}"
                    )
                    status_line.caption(f"Processed {current:,} of {total:,} supported files")

                excluded_paths = [
                    line.strip() for line in excluded_input.splitlines() if line.strip()
                ]
                started = time()
                try:
                    with st.spinner("Scanning the selected folder..."):
                        scanner = scan_and_persist if persist_to_db else scan_folder
                        results = scanner(
                            folder,
                            excluded_paths=excluded_paths,
                            compute_hashes=compute_hashes,
                            extract_content=extract_content,
                            progress_callback=update_progress,
                            recursive=recursive,
                        )

                    progress_bar.progress(1.0, text="Scan complete")
                    elapsed = time() - started
                    st.session_state["scan_results"] = results
                    st.session_state["scan_completed"] = True
                    st.session_state["last_scanned_folder"] = str(folder.resolve())
                    st.session_state["total_files"] = len(results)
                    st.session_state["total_size_mb"] = (
                        sum(item.size for item in results) / 1_000_000
                    )
                    st.session_state["scan_timestamp"] = datetime.now().astimezone()
                    st.session_state["scan_options"] = {
                        "compute_hashes": compute_hashes,
                        "recursive": recursive,
                        "persist_to_db": persist_to_db,
                        "extract_content": extract_content,
                    }
                    st.session_state["duplicate_groups"] = _count_duplicate_groups(results)
                    record_session_activity(
                        "Folder scan",
                        f"{len(results):,} files • {format_size(sum(item.size for item in results))}",
                    )
                    st.success(f"Scan finished in {elapsed:.1f} seconds.")
                    if not results:
                        st.info("No supported files were found in that folder.")
                except InvalidDirectoryError as error:
                    st.error(str(error))
                except DatabaseError:
                    st.error(
                        "The scan could not be saved to the local database. "
                        "Check that the database file is available and writable."
                    )
                except OSError:
                    st.error(
                        "The selected folder could not be read. Check its permissions and try again."
                    )

    render_section_header("Scanned files", icon="files")
    results = st.session_state.get("scan_results")
    if results is None or not st.session_state.get("scan_completed"):
        render_empty_state(
            title="No scan results yet",
            message="Choose a folder above and start a scan to review indexed files.",
            icon="folder",
        )
        return
    if not results:
        render_empty_state(
            title="No supported files found",
            message="This scan completed without finding files in a supported format.",
            icon="files",
        )
        return

    total_size = sum(item.size for item in results)
    duplicates = _count_duplicate_groups(results)
    has_content_extraction = st.session_state.get("scan_options", {}).get("extract_content", False)
    metrics = st.columns(5)
    for column, values in zip(
        metrics,
        [
            ("Files discovered", f"{len(results):,}", "files"),
            ("Total storage", format_size(total_size), "hard_drive"),
            ("Exact duplicates", f"{duplicates:,}", "duplicate"),
            ("Content extraction", "Requested" if has_content_extraction else "Off", "file_text"),
            ("Errors / skipped", "Not reported", "alert_triangle"),
        ],
        strict=True,
    ):
        with column:
            render_kpi_card(*values, subtitle="Current scan")

    category_by_path = {
        row.get("path"): row.get("category")
        for row in st.session_state.get("classification_results", [])
    }
    query = st.text_input("Search scanned files", placeholder="Search by file name or path...")
    filtered_results = [
        item
        for item in results
        if query.casefold() in item.name.casefold()
        or query.casefold() in (item.relative_path or item.path).casefold()
    ]
    table = pd.DataFrame(
        [
            {
                "Filename": item.name,
                "Extension": item.extension or "Unknown",
                "Size": format_size(item.size),
                "Modified": datetime.fromtimestamp(item.modified)
                .astimezone()
                .strftime("%b %d, %Y %I:%M %p"),
                "Path": item.relative_path or item.path,
                "Category": category_by_path.get(item.relative_path or item.path, "Unclassified"),
                "Status": "Scanned",
            }
            for item in filtered_results
        ]
    )
    st.dataframe(table, width="stretch", hide_index=True)


def _count_duplicate_groups(files: list) -> int:
    hashes: dict[str, int] = {}
    for item in files:
        if item.sha256:
            hashes[item.sha256] = hashes.get(item.sha256, 0) + 1
    return sum(count > 1 for count in hashes.values())
