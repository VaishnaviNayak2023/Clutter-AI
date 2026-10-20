"""Reports based on the current scan and classification data."""

import csv
import io
from collections import Counter, defaultdict

import pandas as pd
import streamlit as st

from src.ai_clutter_cleaner.services.reporting import generate_csv_report, generate_report
from src.ai_clutter_cleaner.ui import (
    render_empty_state,
    render_global_header,
    render_page_header,
    render_section_header,
)
from src.ai_clutter_cleaner.ui.data import record_session_activity
from src.ai_clutter_cleaner.ui.layout import format_size


def render_reports() -> None:
    """Render report previews and downloadable files from live scan data."""
    render_global_header()
    render_page_header(
        title="Reports",
        subtitle="Build and export summaries from your current scan.",
        breadcrumb=["Explore", "Reports"],
    )

    files = st.session_state.get("scan_results") or []
    if not files:
        render_empty_state(
            title="No scan data available",
            message="Complete a folder scan before generating a report.",
            icon="folder",
            action_text="Scan Files",
            action_key="reports_go_to_scan",
        )
        if st.session_state.get("reports_go_to_scan"):
            st.session_state["current_page"] = "Scan_Files"
            st.rerun()
        return

    render_section_header("Report configuration", icon="settings")
    report_type = st.selectbox(
        "Report contents",
        [
            "Scan summary",
            "File category breakdown",
            "Duplicate statistics",
            "Storage by extension",
        ],
    )
    format_col, details_col = st.columns(2)
    with format_col:
        report_format = st.selectbox("Export format", ["CSV", "Text"])
    with details_col:
        include_details = st.checkbox(
            "Include detailed file listing",
            value=True,
            help="Include filename, path, extension, and size in CSV exports.",
        )

    records = [
        {
            "name": file.name,
            "path": file.path,
            "extension": file.extension or "Unknown",
            "size": file.size,
            "modified": file.modified,
            "sha256": file.sha256 or "",
        }
        for file in files
    ]
    classification = st.session_state.get("classification_results") or []
    category_counts = Counter(
        row["category"] for row in classification if row["category"] != "Error"
    )
    hash_counts = Counter(file.sha256 for file in files if file.sha256)
    duplicate_groups = {value: count for value, count in hash_counts.items() if count > 1}
    extension_bytes: dict[str, int] = defaultdict(int)
    extension_counts = Counter()
    for file in files:
        extension = file.extension or "Unknown"
        extension_bytes[extension] += file.size
        extension_counts[extension] += 1

    if report_type == "Scan summary":
        preview = generate_report(records)
        summary_rows = [
            ("Metric", "Value"),
            ("Files", str(len(files))),
            ("Storage", format_size(sum(file.size for file in files))),
            ("Duplicate groups", str(len(duplicate_groups))),
        ]
    elif report_type == "File category breakdown":
        if category_counts:
            summary_rows = [("Category", "Files"), *[
                (category, str(count)) for category, count in category_counts.most_common()
            ]]
            preview = "\n".join(f"{category}: {count} files" for category, count in category_counts.most_common())
        else:
            summary_rows = [("Category", "Files")]
            preview = "No classification results are available. Run AI Organization first."
    elif report_type == "Duplicate statistics":
        summary_rows = [
            ("Metric", "Value"),
            ("Exact duplicate groups", str(len(duplicate_groups))),
            ("Files in duplicate groups", str(sum(duplicate_groups.values()))),
        ]
        preview = (
            f"Exact duplicate groups: {len(duplicate_groups)}\n"
            f"Files in duplicate groups: {sum(duplicate_groups.values())}\n"
            "Duplicate groups are determined from SHA-256 hashes."
        )
    else:
        summary_rows = [
            ("Extension", "Files", "Storage"),
            *[
                (extension, str(count), format_size(extension_bytes[extension]))
                for extension, count in extension_counts.most_common()
            ],
        ]
        preview = "\n".join(
            f"{extension}: {count} files, {format_size(extension_bytes[extension])}"
            for extension, count in extension_counts.most_common()
        )

    render_section_header("Preview", icon="file_text")
    with st.container(border=True):
        st.text(preview)

    if st.button(
        "Generate report",
        type="primary",
        icon=":material/download:",
        key="generate_report",
    ):
        if report_format == "CSV":
            if report_type == "Scan summary" and include_details:
                output = generate_csv_report(records)
                filename = "clutterai-file-inventory.csv"
            else:
                buffer = io.StringIO()
                csv.writer(buffer, lineterminator="\n").writerows(summary_rows)
                output = buffer.getvalue()
                filename = "clutterai-report.csv"
            mime_type = "text/csv"
        else:
            output = preview
            filename = "clutterai-report.txt"
            mime_type = "text/plain"
        st.session_state["generated_report"] = (output, filename, mime_type)
        record_session_activity("Report generation", f"{report_type} ({report_format})")
        st.success("Report generated from the current scan data.")

    if st.session_state.get("generated_report"):
        report_data, filename, mime_type = st.session_state["generated_report"]
        st.download_button(
            "Download report",
            data=report_data,
            file_name=filename,
            mime=mime_type,
            icon=":material/download:",
        )

    if report_type == "File category breakdown":
        if category_counts:
            st.dataframe(
                pd.DataFrame(
                    [{"Category": category, "Files": count} for category, count in category_counts.most_common()]
                ),
                width="stretch",
                hide_index=True,
            )
        else:
            st.info("Category reports require current-session classification results.")
