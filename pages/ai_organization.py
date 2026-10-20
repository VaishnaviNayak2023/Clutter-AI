"""Classification review and safe file organization."""

from pathlib import Path
from time import time

import pandas as pd
import plotly.express as px
import streamlit as st

from src.ai_clutter_cleaner.services import extract_text, get_classifier
from src.ai_clutter_cleaner.services.organizer import FileOrganizer
from src.ai_clutter_cleaner.ui import (
    navigate_to_page,
    render_action_card,
    render_empty_state,
    render_global_header,
    render_kpi_card,
    render_page_header,
    render_section_header,
)
from src.ai_clutter_cleaner.ui.data import record_session_activity
from src.ai_clutter_cleaner.ui.theme import CHART_COLORS, COLORS


def render_ai_organization() -> None:
    """Render AI classification review and confirmed organization actions."""
    render_global_header()
    render_page_header(
        title="AI Organization",
        subtitle="Review classifications, evaluate destinations, and organize files safely.",
        breadcrumb=["Workspace", "AI Organization"],
        icon="auto_awesome",
    )

    files = st.session_state.get("scan_results") or []
    if not files:
        metrics = st.columns(4)
        for column, (label, value, icon, subtitle) in zip(
            metrics,
            [("Total files", "—", "files", "To be classified"),
             ("Category distribution", "—", "tag", "Detected by AI"),
             ("Avg. confidence", "—", "target", "Model prediction accuracy"),
             ("Proposed organization", "—", "folder", "Files with new destinations")],
            strict=True,
        ):
            with column:
                render_kpi_card(label, value, icon, subtitle=subtitle)

        distribution_col, confidence_col, insights_col = st.columns([1.05, 1.2, .85])
        for column, title, icon, message in [
            (distribution_col, "Category distribution", "chart_pie", "Your category breakdown will appear after classification."),
            (confidence_col, "Classification confidence", "brain", "Confidence scores will appear after classification."),
        ]:
            with column, st.container(border=True):
                render_section_header(title, icon=icon)
                st.markdown('<div class="chart-placeholder"></div>', unsafe_allow_html=True)
                st.caption(message)
        with insights_col, st.container(border=True):
            render_section_header("AI insights", icon="brain")
            for label, description, icon in [
                ("Duplicate groups found", "Scan files to detect exact copies.", "duplicate"),
                ("Unclassified files", "Classify scanned files to review categories.", "tag"),
                ("Files without category", "Review files that need a useful classification.", "alert_triangle"),
                ("Organization opportunity", "See suggested destinations for your files.", "folder"),
            ]:
                render_action_card(label, description, icon)

        review_col, operations_col = st.columns([2.2, 1])
        with review_col, st.container(border=True):
            render_section_header("Files awaiting review", icon="file_text")
            st.caption("Classified files and destinations will appear here.")
            if render_empty_state(
                "No scan results available",
                "Scan a folder to review classifications and proposed destinations.",
                icon="folder",
                action_text="Go to Scan Files",
                action_key="organization_go_to_scan",
            ):
                navigate_to_page("Scan_Files")
        with operations_col, st.container(border=True):
            render_section_header("Planned file operations", icon="organize")
            for label in ("Move to new location", "Keep in current location", "Requires review", "Destination conflicts"):
                st.markdown(f"<div class='operation-placeholder'><span>{label}</span><b>—</b></div>", unsafe_allow_html=True)
            st.button("Execute Organization", type="primary", disabled=True, width="stretch")
            st.caption("Files remain untouched until you review and confirm an operation.")
        return

    render_section_header("Classification", icon="brain")
    classify_col, clear_col, data_col, mode_col = st.columns([1, 1, 1.5, 1])
    with classify_col:
        classify_requested = st.button(
            "Classify files",
            type="primary",
            icon=":material/auto_awesome:",
            width="stretch",
        )
    with clear_col:
        clear_requested = st.button("Clear results", width="stretch")
    with data_col:
        use_training_data = st.checkbox(
            "Use training_data.csv",
            help="Use the project's generated training data instead of the default training set.",
        )
    with mode_col:
        st.checkbox(
            "Dry Run",
            value=True,
            key="organization_dry_run",
            help="Preview and validate destinations without moving files.",
        )

    if clear_requested:
        st.session_state.pop("classification_results", None)
        st.session_state.pop("organization_editor", None)
        st.rerun()

    if classify_requested:
        training_csv = "training_data.csv" if use_training_data else None
        if use_training_data and not Path(training_csv).is_file():
            st.error("training_data.csv was not found. Generate it before selecting this option.")
            return

        classifier = get_classifier(
            use_real_data=use_training_data,
            training_csv=training_csv,
        )
        progress = st.progress(0, text="Preparing classification")
        predictions = []
        started = time()
        for index, file in enumerate(files):
            progress.progress(
                (index + 1) / len(files), text=f"Classifying {index + 1} of {len(files)}"
            )
            try:
                prediction = classifier.predict(extract_text(Path(file.path)), file.name)
                predictions.append(
                    {
                        "name": file.name,
                        "path": file.relative_path or file.path,
                        "category": prediction.category,
                        "confidence": prediction.confidence,
                        "reason": prediction.reason,
                        "size_bytes": file.size,
                    }
                )
            except (OSError, ValueError, RuntimeError) as error:
                predictions.append(
                    {
                        "name": file.name,
                        "path": file.relative_path or file.path,
                        "category": "Error",
                        "confidence": 0.0,
                        "reason": f"Classification failed: {error}",
                        "size_bytes": file.size,
                    }
                )

        st.session_state["classification_results"] = predictions
        st.session_state.pop("organization_editor", None)
        record_session_activity(
            "AI classification",
            f"{len(predictions):,} files classified in {time() - started:.1f} seconds",
        )
        progress.progress(1.0, text="Classification complete")

    predictions = st.session_state.get("classification_results")
    if not predictions:
        render_empty_state(
            title="Ready to classify",
            message="Classification runs only after you request it. Your files will not be moved automatically.",
            icon="brain",
        )
        return

    result_df = pd.DataFrame(predictions)
    valid_predictions = result_df[result_df["category"] != "Error"]
    distribution = valid_predictions["category"].value_counts()
    average_confidence = (
        valid_predictions["confidence"].mean() if not valid_predictions.empty else 0
    )

    move_count = int((result_df["category"] != "Error").sum())
    metrics = st.columns(4)
    for column, (label, value, icon, subtitle) in zip(
        metrics,
        [
            ("Total files", f"{len(result_df):,}", "files", "To be classified"),
            ("Category distribution", f"{len(distribution):,} categories", "tag", "Detected by AI"),
            ("Avg. confidence", f"{average_confidence:.0%}", "target", "Model prediction accuracy"),
            ("Proposed organization", f"{move_count:,}", "folder", "Files with new destinations"),
        ],
        strict=True,
    ):
        with column:
            render_kpi_card(label, value, icon, subtitle=subtitle)

    pie_col, confidence_col, insight_col = st.columns([1.05, 1.2, .85])
    with pie_col:
        with st.container(border=True):
            render_section_header("Category distribution", icon="chart_pie")
            if not distribution.empty:
                chart_df = distribution.rename_axis("Category").reset_index(name="Files")
                figure = px.pie(
                    chart_df,
                    values="Files",
                    names="Category",
                    hole=0.62,
                    color_discrete_sequence=CHART_COLORS,
                )
                figure.update_layout(
                    height=245,
                    margin=dict(t=5, b=5, l=5, r=5),
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    legend=dict(orientation="h", y=-0.15),
                )
                st.plotly_chart(figure, width="stretch", config={"displayModeBar": False})
            else:
                st.caption("No successful predictions are available to chart.")

    with confidence_col:
        with st.container(border=True):
            render_section_header("Classification confidence", icon="brain")
            confidence_data = (
                valid_predictions.groupby("category", as_index=False)["confidence"]
                .mean()
                .sort_values("confidence", ascending=False)
            )
            if not confidence_data.empty:
                figure = px.bar(
                    confidence_data,
                    x="category",
                    y="confidence",
                    text=confidence_data["confidence"].map(lambda value: f"{value:.0%}"),
                    color_discrete_sequence=[CHART_COLORS[0]],
                )
                figure.update_traces(textposition="outside")
                figure.update_yaxes(
                    range=[0, 1], tickformat=".0%", gridcolor=COLORS["border_light"]
                )
                figure.update_layout(
                    height=245,
                    margin=dict(t=18, b=8, l=4, r=4),
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    showlegend=False,
                    xaxis_title=None,
                    yaxis_title=None,
                )
                st.plotly_chart(figure, width="stretch", config={"displayModeBar": False})
            else:
                st.caption("Confidence data will appear after classification.")

    with insight_col:
        with st.container(border=True):
            render_section_header("AI insights", icon="brain")
            duplicate_groups = st.session_state.get("duplicate_groups", 0)
            for title, description, target, key in [
                (
                    "Duplicate groups found",
                    f"{duplicate_groups} exact groups",
                    "Duplicate_Finder",
                    "org_dup",
                ),
                (
                    "Unclassified files",
                    f"{int((result_df['category'] == 'Error').sum())} need review",
                    "AI_Organization",
                    "org_unc",
                ),
                (
                    "Organization opportunity",
                    f"{move_count} destination suggestions",
                    "AI_Organization",
                    "org_move",
                ),
            ]:
                if st.button(
                    f"{title} · {description}  ›",
                    key=key,
                    width="stretch",
                ):
                    navigate_to_page(target)

    with st.container(border=True):
        render_section_header("Files awaiting review", icon="file_text")
        confidence_threshold = st.slider(
            "High-confidence threshold",
            min_value=0.50,
            max_value=0.99,
            value=0.80,
            step=0.01,
            key="organization_confidence_threshold",
        )
        tabs = st.tabs(["All Files", "High Confidence", "Low Confidence", "Unclassified"])
        filters = [
            result_df,
            result_df[result_df["confidence"] >= confidence_threshold],
            result_df[result_df["confidence"] < confidence_threshold],
            result_df[result_df["category"].isin(["Error", "Unclassified"])],
        ]
        for index, (tab, subset) in enumerate(zip(tabs, filters, strict=True)):
            with tab:
                query = st.text_input(
                    "Search files",
                    key=f"organization_search_{index}",
                    placeholder="Filter by file name...",
                )
                if query:
                    subset = subset[subset["name"].str.contains(query, case=False, na=False)]
                display = subset[["name", "path", "category", "confidence", "reason"]].copy()
                display["confidence"] = display["confidence"].map(lambda value: f"{value:.0%}")
                st.dataframe(display, width="stretch", hide_index=True)
                if not subset.empty:
                    review_path = st.selectbox(
                        "Select a file to review",
                        subset["path"].tolist(),
                        format_func=lambda path: next(
                            row["name"] for row in predictions if row["path"] == path
                        ),
                        key=f"organization_review_path_{index}",
                    )
                    review_row = next(row for row in predictions if row["path"] == review_path)
                    with st.expander("Review classification"):
                        st.caption(
                            f"Confidence: {review_row['confidence']:.0%} · "
                            f"Reason: {review_row['reason']}"
                        )
                        categories = sorted(
                            {
                                row["category"]
                                for row in predictions
                                if row["category"] not in {"Error", "Unclassified"}
                            }
                            | {review_row["category"]}
                        )
                        reviewed_category = st.selectbox(
                            "Category",
                            categories,
                            index=categories.index(review_row["category"]),
                            key=f"organization_review_category_{index}",
                        )
                        if st.button(
                            "Save review",
                            key=f"organization_save_review_{index}",
                        ):
                            updated_predictions = [dict(row) for row in predictions]
                            for row in updated_predictions:
                                if row["path"] == review_path:
                                    row["category"] = reviewed_category
                                    row["reason"] = "Category reviewed by user."
                                    break
                            st.session_state["classification_results"] = updated_predictions
                            st.session_state.pop("organization_editor", None)
                            st.rerun()

    st.divider()
    _render_organization_controls(result_df, files)


def _render_organization_controls(result_df: pd.DataFrame, files: list) -> None:
    """Prepare, validate, and explicitly confirm proposed file moves."""
    render_section_header("Organization preview", icon="organize")
    st.caption(
        "Destinations are suggestions only. Review and select files, validate the dry run, "
        "then confirm before any files are moved."
    )
    dry_run = st.session_state.get("organization_dry_run", True)
    if dry_run:
        st.info("Dry Run is on. Validation will not move or overwrite any files.")
    else:
        st.warning(
            "Dry Run is off. File moves require the confirmation checkbox below and remain "
            "restricted to the selected organization root."
        )
    source_by_relative = {
        (item.relative_path or item.path): Path(item.path).resolve() for item in files
    }
    root_default = st.session_state.get("last_scanned_folder", "")
    root_text = st.text_input(
        "Organization root",
        value=st.session_state.get("organization_root", root_default),
        help="Moves are restricted to this folder; choose a dedicated destination when possible.",
        key="organization_root",
    )
    root = Path(root_text).expanduser() if root_text.strip() else None
    if root is None or not root.is_dir():
        st.info("Choose an existing folder as the organization root to preview destinations.")
        return

    organizer = FileOrganizer(root)
    suggestions = []
    for row in result_df.to_dict("records"):
        source = source_by_relative.get(row["path"])
        if source is None or row["category"] == "Error":
            continue
        destination = organizer.propose_destination(source, row["category"])
        suggestions.append(
            {
                "Select": False,
                "Filename": row["name"],
                "Category": row["category"],
                "Confidence": row["confidence"],
                "Source": str(source),
                "Proposed destination": str(destination),
            }
        )
    if not suggestions:
        render_empty_state(
            title="No move suggestions",
            message="There are no successful classifications with a matching scanned file path.",
            icon="folder",
        )
        return

    confidence_threshold = st.session_state.get("organization_confidence_threshold", 0.8)
    move_count = sum(
        Path(row["Source"]).parent != Path(row["Proposed destination"]).parent
        for row in suggestions
    )
    keep_count = len(suggestions) - move_count
    review_count = sum(row["Confidence"] < confidence_threshold for row in suggestions)
    conflict_count = sum(
        Path(row["Proposed destination"]).exists()
        and Path(row["Proposed destination"]).resolve() != Path(row["Source"]).resolve()
        for row in suggestions
    )
    operation_metrics = st.columns(4)
    for column, (label, value) in zip(
        operation_metrics,
        [
            ("Move to new location", move_count),
            ("Keep in current location", keep_count),
            ("Requires review", review_count),
            ("Destination conflicts", conflict_count),
        ],
        strict=True,
    ):
        with column:
            st.metric(label, value)

    edited = st.data_editor(
        pd.DataFrame(suggestions),
        width="stretch",
        hide_index=True,
        key="organization_editor",
        disabled=["Filename", "Category", "Confidence", "Source"],
        column_config={
            "Select": st.column_config.CheckboxColumn("Select", default=False),
            "Confidence": st.column_config.ProgressColumn(
                "Confidence", min_value=0, max_value=1, format="%.0f%%"
            ),
            "Proposed destination": st.column_config.TextColumn(
                "Proposed destination",
                help="Review or edit the destination before validating the operation.",
            ),
        },
    )
    selected = edited[edited["Select"]]
    preview_col, confirm_col = st.columns([1, 2])
    with preview_col:
        validate_dry_run = st.button(
            "Validate selected moves",
            key="organization_preview",
            width="stretch",
        )
    with confirm_col:
        confirmed = st.checkbox(
            "I reviewed the selected destinations and confirm the file moves.",
            key="organization_confirmed",
        )
        execute_moves = st.button(
            "Execute Organization",
            type="primary",
            key="organization_execute",
            disabled=dry_run or not confirmed or selected.empty,
            width="stretch",
        )

    moves = [
        (Path(row["Source"]), Path(row["Proposed destination"]))
        for row in selected.to_dict("records")
    ]
    if validate_dry_run:
        if not moves:
            st.warning("Select at least one file to validate.")
        else:
            operations = organizer.batch_move(moves, dry_run=True, root_check=root)
            valid = sum(operation.status == "completed" for operation in operations)
            invalid = len(operations) - valid
            st.success(f"Dry run: {valid} moves valid; {invalid} need attention.")
            for operation in operations:
                if operation.status == "failed":
                    st.error(f"{operation.source_path}: {operation.error_message}")

    if execute_moves:
        operations = organizer.batch_move(moves, dry_run=False, root_check=root)
        st.session_state.setdefault("organization_operations", []).extend(operations)
        moved = sum(operation.status == "completed" for operation in operations)
        failed = len(operations) - moved
        record_session_activity(
            "Organization",
            f"{moved} files moved; {failed} failed",
            "Completed" if not failed else "Review",
        )
        if failed:
            st.warning(f"{moved} files moved; {failed} moves failed.")
            for operation in operations:
                if operation.status == "failed":
                    st.error(f"{operation.source_path}: {operation.error_message}")
        else:
            st.success(f"{moved} files moved. Completed moves can be undone in this session.")

    undoable = [
        operation
        for operation in st.session_state.get("organization_operations", [])
        if operation.status == "completed"
    ]
    if undoable:
        st.markdown("#### Undo a completed move")
        selected_operation = st.selectbox(
            "Completed move",
            undoable,
            format_func=lambda operation: (
                f"{operation.source_path.name} → {operation.destination_path}"
            ),
            key="organization_undo_selection",
        )
        if st.button("Undo selected move", key="organization_undo"):
            undo_manager = FileOrganizer(root)
            undo_manager.operations = st.session_state["organization_operations"]
            result = undo_manager.undo_move(selected_operation.operation_id)
            if result and result.status == "undone":
                st.success(f"Restored {result.source_path.name} to its original location.")
            else:
                st.error(
                    result.error_message if result else "The selected move could not be found."
                )
