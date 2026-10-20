"""Overview dashboard."""

from collections import Counter

import pandas as pd
import plotly.express as px
import streamlit as st

from src.ai_clutter_cleaner.ui import (
    navigate_to_page,
    render_action_card,
    render_global_header,
    render_kpi_card,
    render_page_header,
    render_section_header,
)
from src.ai_clutter_cleaner.ui.layout import format_size
from src.ai_clutter_cleaner.ui.theme import CHART_COLORS, COLORS


def render_dashboard() -> None:
    """Render workspace metrics and actionable summaries from current data."""
    render_global_header()
    render_page_header(
        title="Your digital workspace",
        subtitle=(
            "Understand your files, discover duplicates, and organize your "
            "digital workspace with AI."
        ),
        breadcrumb=["Workspace", "Overview"],
    )

    files = st.session_state.get("scan_results") or []
    total_size = sum(item.size for item in files)
    hash_counts = Counter(item.sha256 for item in files if item.sha256)
    exact_groups = sum(count > 1 for count in hash_counts.values())
    classification = st.session_state.get("classification_results")
    classified_count = len(classification) if classification is not None else 0
    semantic = st.session_state.get("semantic_results") or {}
    similar_count = len(semantic.get("matches", []))
    operations = st.session_state.get("organization_operations", [])
    organized_count = sum(operation.status == "completed" for operation in operations)
    unclassified_count = sum(
        row.get("category") in {"Unclassified", "Error"} for row in classification or []
    )

    kpis = [
        ("Total Files", f"{len(files):,}", "files", "Indexed in current scan"),
        ("Storage Used", format_size(total_size), "hard_drive", "Current scan size"),
        ("Exact Duplicate Groups", f"{exact_groups:,}", "duplicate", "SHA-256 matches"),
        ("Files Organized", f"{organized_count:,}", "organize", "Completed moves"),
    ]
    columns = st.columns(4)
    for column, (title, value, icon, subtitle) in zip(columns, kpis, strict=True):
        with column:
            render_kpi_card(title, value, icon, subtitle=subtitle)

    breakdown_col, insights_col = st.columns([1.15, 1])
    with breakdown_col, st.container(border=True):
        render_section_header("Storage breakdown", icon="chart_pie")
        measure = st.radio(
            "Breakdown metric",
            ["File Count", "Storage Size"],
            horizontal=True,
            label_visibility="collapsed",
            key="dashboard_breakdown_metric",
        )
        extension_counts = Counter((item.extension or "Unknown") for item in files)
        extension_sizes: dict[str, int] = {}
        for item in files:
            extension = item.extension or "Unknown"
            extension_sizes[extension] = extension_sizes.get(extension, 0) + item.size

        classifications = {
            row.get("path"): row.get("category", "Unclassified") for row in classification or []
        }
        category_counts: Counter[str] = Counter()
        category_sizes: dict[str, int] = {}
        for item in files:
            category = classifications.get(item.relative_path or item.path, "Unclassified")
            category_counts[category] += 1
            category_sizes[category] = category_sizes.get(category, 0) + item.size
        selected_counts = category_counts if measure == "File Count" else category_sizes
        selected_total = len(files) if measure == "File Count" else total_size
        chart_data = pd.DataFrame(
            [
                {
                    "Category": category,
                    "Value": value,
                    "Files": category_counts[category],
                    "Share": value / selected_total if selected_total else 0,
                }
                for category, value in sorted(
                    selected_counts.items(), key=lambda item: item[1], reverse=True
                )[:7]
            ]
        )
        if not files:
            pie_col, legend_col = st.columns([1, 1.15])
            with pie_col:
                st.markdown('<div class="chart-placeholder"></div>', unsafe_allow_html=True)
            with legend_col:
                for category in ("Documents", "Code", "Data", "Media", "Archives", "Other"):
                    st.markdown(
                        f"<div class='legend-placeholder'><span>{category}</span><b>—</b></div>",
                        unsafe_allow_html=True,
                    )
            render_section_header("Files by extension", icon="files")
            st.markdown('<div class="bar-chart-placeholder"></div>', unsafe_allow_html=True)
            st.caption("Scan a folder to populate the charts with your files.")
            if st.button("Scan a folder", key="dashboard_first_scan", type="primary"):
                navigate_to_page("Scan_Files")
        else:
            pie_col, legend_col = st.columns([1, 1.15])
            with pie_col:
                figure = px.pie(
                    chart_data,
                    values="Value",
                    names="Category",
                    hole=0.62,
                    color_discrete_sequence=CHART_COLORS,
                )
                figure.update_layout(
                    height=230,
                    margin=dict(t=4, b=4, l=2, r=2),
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    showlegend=False,
                    annotations=[
                        dict(
                            text=f"{len(files):,}<br><span style='font-size:11px'>files</span>",
                            x=0.5,
                            y=0.5,
                            showarrow=False,
                            font=dict(size=17, color=COLORS["primary_text"]),
                        )
                    ],
                )
                st.plotly_chart(figure, width="stretch", config={"displayModeBar": False})
            with legend_col:
                for index, row in enumerate(chart_data.to_dict("records")):
                    amount = (
                        f"{row['Files']:,}"
                        if measure == "File Count"
                        else format_size(category_sizes[row["Category"]])
                    )
                    label_col, share_col, amount_col = st.columns([2.2, .8, .8])
                    with label_col:
                        st.markdown(
                            f"<span class='legend-dot' style='--legend-color:{CHART_COLORS[index % len(CHART_COLORS)]}'></span>"
                            f"<span class='legend-label'>{row['Category']}</span>",
                            unsafe_allow_html=True,
                        )
                    with share_col:
                        st.caption(f"{row['Share']:.0%}")
                    with amount_col:
                        st.caption(amount)
            render_section_header("Files by extension", icon="files")
            extension_data = pd.DataFrame(
                [
                    {"Extension": extension, "Files": count}
                    for extension, count in extension_counts.most_common(8)
                ]
            )
            figure = px.bar(
                extension_data,
                x="Extension",
                y="Files",
                color_discrete_sequence=[CHART_COLORS[0]],
            )
            figure.update_layout(
                height=145,
                margin=dict(t=0, b=0, l=0, r=0),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                showlegend=False,
                xaxis_title=None,
                yaxis_title=None,
            )
            figure.update_traces(marker_line_width=0)
            figure.update_xaxes(showgrid=False)
            figure.update_yaxes(gridcolor=COLORS["border_light"])
            st.plotly_chart(figure, width="stretch", config={"displayModeBar": False})

    with insights_col, st.container(border=True):
        render_section_header("AI insights", icon="brain")
        insight_items = [
            (
                "Duplicate groups found",
                f"{exact_groups} exact groups found using SHA-256",
                "duplicate",
                "Duplicate_Finder",
            ),
            (
                "Similar documents",
                f"{similar_count} semantic pairs meet the selected threshold",
                "file_text",
                "Duplicate_Finder",
            ),
            (
                "Unclassified files",
                f"{unclassified_count} files need classification review",
                "brain",
                "AI_Organization",
            ),
            (
                "Files without category",
                f"{max(len(files) - classified_count, 0)} files have no classification yet",
                "files",
                "AI_Organization",
            ),
            (
                "Organization opportunity",
                f"{max(len(files) - organized_count, 0)} files are available for review",
                "organize",
                "AI_Organization",
            ),
        ]
        for index, (title, description, icon, target) in enumerate(insight_items):
            if render_action_card(
                title=title,
                description=description,
                icon=icon,
                value=None,
                action_label="Open",
                action_key=f"dashboard_insight_{index}",
            ):
                navigate_to_page(target)

    activity_col, actions_col = st.columns([1.65, 1])
    with activity_col, st.container(border=True):
        render_section_header("Recent activity", icon="clock")
        activity = st.session_state.get("activity_log", [])
        if activity:
            st.dataframe(
                pd.DataFrame(activity[:8]),
                width="stretch",
                hide_index=True,
                column_config={
                    "Action": st.column_config.TextColumn(width="medium"),
                    "Details": st.column_config.TextColumn(width="large"),
                    "Time": st.column_config.TextColumn(width="medium"),
                    "Status": st.column_config.TextColumn(width="small"),
                },
            )
        else:
            st.caption("Scan and organization activity will appear here.")
        if st.button("View history", key="dashboard_history"):
            navigate_to_page("History")

    with actions_col, st.container(border=True):
        render_section_header("Quick actions", icon="arrow_up_right")
        for label, target, icon in [
            ("Scan a folder", "Scan_Files", "folder_open"),
            ("Find duplicates", "Duplicate_Finder", "content_copy"),
            ("Organize with AI", "AI_Organization", "psychology"),
            ("Search files", "Search_Explorer", "search"),
            ("Generate report", "Reports", "description"),
        ]:
            if st.button(
                label,
                key=f"dashboard_action_{target}",
                icon=f":material/{icon}:",
                width="stretch",
            ):
                navigate_to_page(target)
