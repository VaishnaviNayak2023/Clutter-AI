"""Streamlit-friendly presentation components."""

from html import escape

import streamlit as st

from src.ai_clutter_cleaner.ui.components import render_icon
from src.ai_clutter_cleaner.ui.theme import COLORS


def _icon(name: str, size: int, color: str | None = None) -> str:
    return render_icon(name, size=size, color=color).replace("\n", "").strip()


def render_page_header(
    title: str,
    subtitle: str | None = None,
    breadcrumb: list[str] | None = None,
    actions: list | None = None,
    icon: str | None = None,
) -> None:
    if breadcrumb:
        st.markdown(
            f'<nav class="page-breadcrumb" aria-label="Breadcrumb">'
            f'{escape(" / ".join(breadcrumb))}</nav>',
            unsafe_allow_html=True,
        )
    icon_markup = f'<span class="page-title-icon">{_icon(icon, 28)}</span>' if icon else ""
    st.markdown(
        f'<h1 class="page-title">{icon_markup}<span>{escape(title)}</span></h1>',
        unsafe_allow_html=True,
    )
    if subtitle:
        st.markdown(
            f'<p class="page-subtitle">{escape(subtitle)}</p>',
            unsafe_allow_html=True,
        )

    if actions:
        columns = st.columns(len(actions))
        for column, action in zip(columns, actions, strict=False):
            with column:
                if st.button(
                    action["label"],
                    key=action.get("key"),
                    width="stretch",
                ) and action.get("callback"):
                    action["callback"]()


def render_kpi_card(
    title: str,
    value: str | int | float,
    icon: str,
    subtitle: str | None = None,
    delta: str | None = None,
    color: str | None = None,
) -> None:
    icon_markup = _icon(icon, 23, color or COLORS["primary_accent"])
    subtitle_markup = f'<div class="kpi-subtitle">{escape(subtitle)}</div>' if subtitle else ""
    delta_markup = f'<div class="kpi-delta">{escape(delta)}</div>' if delta else ""
    st.markdown(
        f'<div class="kpi-card"><div class="kpi-icon">{icon_markup}</div>'
        f'<div class="kpi-label">{escape(str(title))}</div>'
        f'<div class="kpi-value">{escape(str(value))}</div>'
        f"{subtitle_markup}{delta_markup}</div>",
        unsafe_allow_html=True,
    )


def render_section_header(title: str, icon: str | None = None) -> None:
    icon_markup = f'<span class="section-icon">{_icon(icon, 18)}</span>' if icon else ""
    st.markdown(
        f'<h2 class="section-heading">{icon_markup}<span>{escape(title)}</span></h2>',
        unsafe_allow_html=True,
    )


def render_status_badge(status: str, size: str = "md") -> None:
    del size
    safe_status = escape(status.replace("_", " ").title())
    status_class = status.lower().replace(" ", "-")
    st.markdown(
        f'<span class="status-badge status-{escape(status_class)}">{safe_status}</span>',
        unsafe_allow_html=True,
    )


def render_empty_state(
    title: str,
    message: str,
    icon: str = "folder",
    action_text: str | None = None,
    action_key: str | None = None,
) -> bool:
    st.markdown(
        f'<section class="empty-state"><div class="empty-state-icon" aria-hidden="true">'
        f'{_icon(icon, 42)}</div>'
        f'<h2 class="empty-state-title">{escape(title)}</h2>'
        f'<p class="empty-state-message">{escape(message)}</p></section>',
        unsafe_allow_html=True,
    )
    if action_text and action_key:
        return st.button(action_text, key=action_key, type="primary")
    return False


def render_insight_card(
    title: str,
    description: str,
    icon: str,
    value: str | None = None,
    action_label: str | None = None,
    action_key: str | None = None,
) -> bool:
    value_markup = f'<div class="insight-value">{escape(value)}</div>' if value else ""
    st.markdown(
        f'<div class="insight-card"><div class="insight-header">{_icon(icon, 20)}'
        f"<span>{escape(title)}</span></div>{value_markup}"
        f'<div class="insight-description">{escape(description)}</div></div>',
        unsafe_allow_html=True,
    )
    if action_label and action_key:
        return st.button(action_label, key=action_key, width="stretch")
    return False


def render_card(
    content: str | None = None,
    title: str | None = None,
    icon: str | None = None,
) -> None:
    with st.container(border=True):
        if title:
            render_section_header(title, icon)
        if content:
            st.markdown(content)


def render_action_card(
    title: str,
    description: str,
    icon: str,
    value: str | None = None,
    action_label: str | None = None,
    action_key: str | None = None,
) -> bool:
    value_markup = f'<div class="action-value">{escape(value)}</div>' if value else ""
    if action_label and action_key:
        card_col, action_col = st.columns([7, 0.65], vertical_alignment="center")
        with card_col:
            _render_action_card_markup(title, description, icon, value_markup)
        with action_col:
            return st.button("›", key=action_key, help=action_label, width="stretch")
    _render_action_card_markup(title, description, icon, value_markup)
    return False


def _render_action_card_markup(
    title: str,
    description: str,
    icon: str,
    value_markup: str,
) -> None:
    st.markdown(
        f'<div class="action-card"><span class="action-icon">{_icon(icon, 20)}</span>'
        f'<div class="action-copy">{value_markup}<div class="action-title">{escape(title)}</div>'
        f'<div class="action-description">{escape(description)}</div></div>'
        f'<span class="action-arrow">{_icon("chevron_right", 16)}</span></div>',
        unsafe_allow_html=True,
    )
