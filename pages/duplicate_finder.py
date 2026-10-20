"""Exact duplicate and semantic similarity review."""

from collections import defaultdict
from pathlib import Path

import pandas as pd
import streamlit as st

from src.ai_clutter_cleaner.services import extract_text, find_similar_documents
from src.ai_clutter_cleaner.ui import (
    navigate_to_page,
    render_action_card,
    render_empty_state,
    render_global_header,
    render_kpi_card,
    render_page_header,
    render_section_header,
)
from src.ai_clutter_cleaner.ui.data import get_preference, record_session_activity
from src.ai_clutter_cleaner.ui.layout import format_size


def render_duplicate_finder() -> None:
    """Render duplicate groups derived from actual scan hashes and extracted text."""
    render_global_header()
    render_page_header(
        title="Duplicate Finder",
        subtitle="Find exact and similar files using SHA-256 hashes and semantic analysis.",
        breadcrumb=["Workspace", "Duplicate Finder"],
        icon="duplicate",
    )

    files = st.session_state.get("scan_results") or []
    if not files:
        metrics = st.columns(4)
        for column, (label, value, icon, subtitle) in zip(
            metrics,
            [("Exact duplicate groups", "—", "duplicate", "Found using SHA-256 hashes"),
             ("Similar file groups", "—", "brain", "Found using semantic similarity"),
             ("Total duplicate files", "—", "files", "Across all groups"),
             ("Potential storage savings", "—", "hard_drive", "Estimated exact duplicates")],
            strict=True,
        ):
            with column:
                render_kpi_card(label, value, icon, subtitle=subtitle)

        exact_col, similar_col = st.columns([1.2, 1])
        with exact_col, st.container(border=True):
            render_section_header("Exact duplicates", icon="duplicate")
            st.caption("Files with identical content (SHA-256 hash match)")
            render_empty_state(
                "No scan results available",
                "Scan a folder with SHA-256 hashing enabled to find exact copies.",
                icon="folder",
            )
        with similar_col, st.container(border=True):
            render_section_header("Similar files (semantic similarity)", icon="brain")
            threshold = st.slider(
                "Similarity threshold", .50, .99,
                value=get_preference("duplicates.similarity_threshold", .75),
                step=.01, key="similarity_threshold_empty",
            )
            st.caption(f"Files with related content above the {threshold:.0%} threshold.")
            render_empty_state(
                "No similarity analysis yet",
                "Scan a folder before comparing document content.",
                icon="file_text",
            )
            st.button("Analyze documents", type="primary", disabled=True, width="stretch")

        groups_col, insights_col = st.columns([1.2, 1])
        with groups_col, st.container(border=True):
            render_section_header("Duplicate file groups", icon="files")
            st.caption("A detailed view of all exact duplicate groups")
            st.dataframe(
                pd.DataFrame(columns=["Group", "Files", "Total size", "Type", "Actions"]),
                width="stretch", hide_index=True,
            )
        with insights_col, st.container(border=True):
            render_section_header("AI insights", icon="lightbulb")
            render_action_card("Duplicate groups found", "Run a scan to identify identical files.", "duplicate")
            render_action_card("Similar documents", "Compare document content with semantic analysis.", "file_text")
            render_action_card("Organization opportunity", "Review file categories in AI Organization.", "folder")
        if st.button("Go to Scan Files", type="primary", key="duplicates_go_to_scan"):
            navigate_to_page("Scan_Files")
        return

    hash_groups: dict[str, list] = defaultdict(list)
    for file in files:
        if file.sha256:
            hash_groups[file.sha256].append(file)
    exact_groups = {value: group for value, group in hash_groups.items() if len(group) > 1}
    exact_file_count = sum(len(group) for group in exact_groups.values())
    potential_savings = sum(sum(file.size for file in group[1:]) for group in exact_groups.values())
    semantic = st.session_state.get("semantic_results") or {}
    matches = semantic.get("matches", [])

    metrics = st.columns(4)
    for column, (title, value, icon, subtitle) in zip(
        metrics,
        [
            ("Exact duplicate groups", len(exact_groups), "duplicate", "Identical SHA-256"),
            ("Similar file groups", len(matches), "brain", "Semantic matches"),
            ("Total duplicate files", exact_file_count, "files", "Exact matches only"),
            (
                "Potential storage savings",
                format_size(potential_savings),
                "hard_drive",
                "Extra exact copies",
            ),
        ],
        strict=True,
    ):
        with column:
            render_kpi_card(
                title,
                f"{value:,}" if isinstance(value, int) else value,
                icon,
                subtitle=subtitle,
            )

    exact_col, similar_col = st.columns([1.2, 1])
    with exact_col, st.container(border=True):
        render_section_header("Files with identical content", icon="duplicate")
        if not exact_groups:
            render_empty_state(
                title="No exact duplicates detected",
                message=(
                    "No matching hashes were found. Hashes are only available for files "
                    "scanned with SHA-256 enabled."
                ),
                icon="circle_check",
            )
        else:
            st.caption(
                f"{len(exact_groups)} groups • {exact_file_count} files • "
                f"{format_size(potential_savings)} potentially reclaimable from extra copies"
            )
            group_query = st.text_input(
                "Search duplicate groups",
                key="duplicate_group_query",
                placeholder="Filter groups by file name or path...",
            )
            group_rows = []
            for index, (hash_value, group) in enumerate(exact_groups.items(), start=1):
                group_rows.append(
                    {
                        "Group": f"Group {index}",
                        "Files": len(group),
                        "Total size": format_size(sum(item.size for item in group)),
                        "Type": ", ".join(sorted({item.extension or "Unknown" for item in group})),
                    }
                )
                if group_query and not any(
                    group_query.casefold() in item.name.casefold()
                    or group_query.casefold() in item.path.casefold()
                    for item in group
                ):
                    continue
                with st.expander(
                    f"Group {index} · {len(group)} files · "
                    f"{format_size(sum(f.size for f in group))}",
                    expanded=index == 1,
                ):
                    st.caption(f"SHA-256: {hash_value}")
                    st.dataframe(
                        pd.DataFrame(
                            [
                                {
                                    "Filename": file.name,
                                    "Path": file.path,
                                    "Size": format_size(file.size),
                                    "Modified": pd.to_datetime(
                                        file.modified, unit="s", utc=True
                                    ).tz_convert(None),
                                }
                                for file in group
                            ]
                        ),
                        width="stretch",
                        hide_index=True,
                    )
                    st.caption(
                        "Files in this group are byte-identical. Review paths before taking any action."
                    )
            with st.expander("Duplicate file groups", expanded=True):
                st.dataframe(pd.DataFrame(group_rows), width="stretch", hide_index=True)

    with similar_col, st.container(border=True):
        render_section_header("Related documents", icon="brain")
        threshold = st.slider(
            "Similarity threshold",
            min_value=0.50,
            max_value=0.99,
            value=get_preference("duplicates.similarity_threshold", 0.75),
            step=0.01,
            key="similarity_threshold",
            help="The existing embedding model returns content-similarity scores, not exact matches.",
        )
        run_col, clear_col = st.columns(2)
        with run_col:
            run_similarity = st.button(
                "Analyze documents",
                type="primary",
                icon=":material/psychology:",
                width="stretch",
            )
        with clear_col:
            clear_similarity = st.button("Clear results", width="stretch")

        if clear_similarity:
            st.session_state.pop("semantic_results", None)
            st.rerun()
        if run_similarity:
            progress = st.progress(0, text="Extracting document text")
            texts = []
            for index, file in enumerate(files):
                progress.progress(
                    (index + 1) / len(files), text=f"Extracting {index + 1} of {len(files)}"
                )
                texts.append(extract_text(Path(file.path)))
            progress.progress(0.8, text="Comparing document embeddings")
            results = find_similar_documents(texts, threshold=0.50)
            st.session_state["semantic_results"] = {
                "matches": results,
                "file_paths": files,
                "texts": texts,
                "threshold": 0.50,
            }
            record_session_activity(
                "Similarity analysis",
                f"{len(results)} similar pairs at a {threshold:.0%} threshold",
            )
            matches = results
            semantic = st.session_state["semantic_results"]
            progress.progress(1.0, text="Analysis complete")

        matches = [
            item for item in semantic.get("matches", []) if item.similarity_score >= threshold
        ]
        if not semantic:
            render_empty_state(
                title="No similarity analysis yet",
                message="Run semantic analysis to compare extracted document text. The first run may download the configured model.",
                icon="file_text",
            )
        elif not matches:
            render_empty_state(
                title="No similar documents found",
                message=f"No document pairs met the selected {semantic.get('threshold', threshold):.0%} threshold.",
                icon="circle_check",
            )
        else:
            file_paths = semantic["file_paths"]
            average_similarity = sum(item.similarity_score for item in matches) / len(matches)
            pair_cols = st.columns(2)
            pair_cols[0].metric("Similar pairs", len(matches))
            pair_cols[1].metric("Average similarity", f"{average_similarity:.0%}")
            for match in matches:
                file_a = file_paths[match.file_id_a]
                file_b = file_paths[match.file_id_b]
                with st.container(border=True):
                    st.markdown(
                        f"**{file_a.name}** and **{file_b.name}** · "
                        f"{match.similarity_score:.0%} similar"
                    )
                    st.caption(f"{file_a.path}  |  {file_b.path}")
                    st.caption("Semantic similarity does not mean the files are byte-identical.")

    insight_col, action_col = st.columns([2, 1])
    with insight_col:
        with st.container(border=True):
            render_section_header("AI insights", icon="brain")
            st.markdown(
                f"**{len(exact_groups)} duplicate groups found** · "
                f"{len(matches)} semantic pairs meet the selected threshold."
            )
            st.caption(
                "Unknown classifications and organization suggestions are available in AI Organization."
            )
    with action_col:
        if st.button(
            "Review AI organization",
            key="duplicates_to_organization",
            width="stretch",
        ):
            navigate_to_page("AI_Organization")
