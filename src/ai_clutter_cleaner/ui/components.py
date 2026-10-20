"""UI components for ClutterAI dashboard."""

import streamlit as st

from src.ai_clutter_cleaner.ui.theme import (
    BORDER_RADIUS,
    COLORS,
    FONTS,
    SHADOWS,
    SPACING,
)

# SVG Icons
ICONS = {
    "layout_dashboard": """
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <rect width="7" height="9" x="3" y="3" rx="1"/>
        <rect width="7" height="5" x="14" y="3" rx="1"/>
        <rect width="7" height="9" x="14" y="12" rx="1"/>
        <rect width="7" height="5" x="3" y="16" rx="1"/>
    </svg>
    """,
    "folder": """
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M4 20h16a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-7.93a2 2 0 0 1-1.66-.9l-.82-1.2A2 2 0 0 0 7.93 3H4a2 2 0 0 0-2 2v13c0 1.1.9 2 2 2Z"/>
    </svg>
    """,
    "files": """
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/>
        <path d="M14 2v4a2 2 0 0 0 2 2h4"/>
    </svg>
    """,
    "search": """
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="11" cy="11" r="8"/>
        <path d="m21 21-4.3-4.3"/>
    </svg>
    """,
    "scan": """
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M3 7V5a2 2 0 0 1 2-2h2"/>
        <path d="M17 3h2a2 2 0 0 1 2 2v2"/>
        <path d="M21 17v2a2 2 0 0 1-2 2h-2"/>
        <path d="M7 21H5a2 2 0 0 1-2-2v-2"/>
    </svg>
    """,
    "brain": """
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M9.5 2A2.5 2.5 0 0 1 12 4.5v15a2.5 2.5 0 0 1-4.96.44 2.5 2.5 0 0 1-2.96-3.08 3 3 0 0 1-.34-5.58 2.5 2.5 0 0 1 1.32-4.24 2.5 2.5 0 0 1 1.98-3A2.5 2.5 0 0 1 9.5 2Z"/>
        <path d="M14.5 2A2.5 2.5 0 0 0 12 4.5v15a2.5 2.5 0 0 0 4.96.44 2.5 2.5 0 0 0 2.96-3.08 3 3 0 0 0 .34-5.58 2.5 2.5 0 0 0-1.32-4.24 2.5 2.5 0 0 0-1.98-3A2.5 2.5 0 0 0 14.5 2Z"/>
    </svg>
    """,
    "auto_awesome": """
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="m12 3 1.9 5.8L20 11l-6.1 2.2L12 19l-1.9-5.8L4 11l6.1-2.2L12 3Z"/>
        <path d="m19 14 1.1 2.2L22 17l-1.9.8L19 20l-1-2.2L16 17l2-.8 1-2.2ZM5 3l.9 2.1L8 6l-2.1.9L5 9l-.9-2.1L2 6l2.1-.9L5 3Z"/>
    </svg>
    """,
    "tag": """
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M20.6 13.4 13.4 20.6a2 2 0 0 1-2.8 0L3.4 13.4a2 2 0 0 1-.6-1.4V5a2 2 0 0 1 2-2h7a2 2 0 0 1 1.4.6l7.4 7a2 2 0 0 1 0 2.8Z"/>
        <circle cx="7.5" cy="7.5" r="1"/>
    </svg>
    """,
    "lightbulb": """
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M9 18h6M10 22h4M8 14.5a7 7 0 1 1 8 0c-1 .7-1.5 1.6-1.5 2.5h-5c0-.9-.5-1.8-1.5-2.5Z"/>
    </svg>
    """,
    "copy": """
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <rect width="14" height="14" x="8" y="8" rx="2" ry="2"/>
        <path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/>
    </svg>
    """,
    "hard_drive": """
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <line x1="22" x2="2" y1="12" y2="12"/>
        <path d="M5.45 5.11 2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z"/>
        <line x1="6" x2="6" y1="16" y2="16"/>
        <line x1="10" x2="10" y1="16" y2="16"/>
        <line x1="14" x2="14" y1="16" y2="16"/>
        <line x1="18" x2="18" y1="16" y2="16"/>
    </svg>
    """,
    "chart_pie": """
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M21.21 15.89A10 10 0 1 1 8 2.83"/>
        <path d="M22 12A10 10 0 0 0 12 2v10z"/>
    </svg>
    """,
    "history": """
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 12"/>
        <path d="M3 3v9h9"/>
    </svg>
    """,
    "settings": """
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.1a2 2 0 0 1-1-1.72v-.51a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/>
        <circle cx="12" cy="12" r="3"/>
    </svg>
    """,
    "file_text": """
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/>
        <path d="M14 2v4a2 2 0 0 0 2 2h4"/>
        <path d="M10 9H8"/>
        <path d="M16 13H8"/>
        <path d="M16 17H8"/>
    </svg>
    """,
    "shield_check": """
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10"/>
        <path d="m9 12 2 2 4-4"/>
    </svg>
    """,
    "chevron_right": """
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="m9 18 6-6-6-6"/>
    </svg>
    """,
    "arrow_up_right": """
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M7 17L17 7"/>
        <path d="M7 7h10v10"/>
    </svg>
    """,
    "circle_check": """
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="10"/>
        <path d="m9 12 2 2 4-4"/>
    </svg>
    """,
    "alert_triangle": """
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/>
        <path d="M12 9v4"/>
        <path d="M12 17h.01"/>
    </svg>
    """,
    "duplicate": """
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <rect width="8" height="8" x="8" y="8" rx="1"/>
        <path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/>
    </svg>
    """,
    "organize": """
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M3 6h18"/>
        <path d="M7 12h10"/>
        <path d="M10 18h4"/>
    </svg>
    """,
    "clock": """
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="10"/>
        <polyline points="12 6 12 12 16 14"/>
    </svg>
    """,
    "download": """
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
        <polyline points="7 10 12 15 17 10"/>
        <line x1="12" x2="12" y1="15" y2="3"/>
    </svg>
    """,
    "trash": """
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M3 6h18"/>
        <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/>
        <path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/>
    </svg>
    """,
    "refresh": """
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/>
        <path d="M21 3v5h-5"/>
        <path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"/>
        <path d="M8 16H3v5"/>
    </svg>
    """,
    "database": """
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <ellipse cx="12" cy="5" rx="9" ry="3"/>
        <path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/>
        <path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/>
    </svg>
    """,
    "target": """
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="10"/>
        <circle cx="12" cy="12" r="6"/>
        <circle cx="12" cy="12" r="2"/>
    </svg>
    """,
}


def render_icon(name: str, size: int = 20, color: str = None) -> str:
    """Render an SVG icon."""
    svg = ICONS.get(name, ICONS["file_text"])
    if color:
        svg = svg.replace('stroke="currentColor"', f'stroke="{color}"')
    svg = svg.replace('width="20"', f'width="{size}"')
    svg = svg.replace('height="20"', f'height="{size}"')
    return svg


def render_page_header(
    title: str,
    subtitle: str = None,
    breadcrumb: list[str] = None,
    actions: list = None,
):
    """Render a professional page header."""
    st.markdown(
        f"""
        <style>
        .page-header {{
            margin-bottom: {SPACING["lg"]};
        }}
        .page-breadcrumb {{
            color: {COLORS["secondary_text"]};
            font-size: {FONTS["metadata"]};
            margin-bottom: {SPACING["sm"]};
        }}
        .page-title {{
            font-size: {FONTS["page_heading"]};
            font-weight: 600;
            color: {COLORS["primary_text"]};
            margin: 0 0 {SPACING["xs"]} 0;
        }}
        .page-subtitle {{
            font-size: {FONTS["body_text"]};
            color: {COLORS["secondary_text"]};
            margin: 0;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    if breadcrumb:
        breadcrumb_html = " / ".join(breadcrumb)
        st.markdown(
            f'<div class="page-breadcrumb">{breadcrumb_html}</div>',
            unsafe_allow_html=True,
        )

    st.markdown(f'<div class="page-title">{title}</div>', unsafe_allow_html=True)

    if subtitle:
        st.markdown(f'<div class="page-subtitle">{subtitle}</div>', unsafe_allow_html=True)

    if actions:
        cols = st.columns(len(actions))
        for col, action in zip(cols, actions):
            with col:
                if st.button(action["label"], key=action.get("key"), width="stretch"):
                    if action.get("callback"):
                        action["callback"]()


def render_kpi_card(
    title: str,
    value: str | int | float,
    icon: str,
    subtitle: str = None,
    delta: str = None,
    color: str = None,
):
    """Render a KPI metric card."""
    card_color = color or COLORS["primary_accent"]

    st.markdown(
        f"""
        <style>
        .kpi-card {{
            background-color: {COLORS["card_background"]};
            border: 1px solid {COLORS["border"]};
            border-radius: {BORDER_RADIUS["lg"]};
            padding: {SPACING["md"]};
            box-shadow: {SHADOWS["md"]};
            transition: all 0.2s ease;
        }}
        .kpi-card:hover {{
            box-shadow: {SHADOWS["lg"]};
            transform: translateY(-2px);
        }}
        .kpi-icon {{
            margin-bottom: {SPACING["sm"]};
            color: {card_color};
        }}
        .kpi-label {{
            font-size: {FONTS["metadata"]};
            color: {COLORS["secondary_text"]};
            font-weight: 500;
            margin-bottom: {SPACING["xs"]};
        }}
        .kpi-value {{
            font-size: {FONTS["kpi_value"]};
            font-weight: 600;
            color: {COLORS["primary_text"]};
            margin-bottom: {SPACING["xs"]};
        }}
        .kpi-subtitle {{
            font-size: {FONTS["caption"]};
            color: {COLORS["muted_text"]};
        }}
        .kpi-delta {{
            font-size: {FONTS["caption"]};
            color: {COLORS["success"]};
            margin-top: {SPACING["xs"]};
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    icon_html = render_icon(icon, size=24)
    delta_html = f'<div class="kpi-delta">{delta}</div>' if delta else ""
    subtitle_html = f'<div class="kpi-subtitle">{subtitle}</div>' if subtitle else ""

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon">{icon_html}</div>
            <div class="kpi-label">{title}</div>
            <div class="kpi-value">{value}</div>
            {subtitle_html}
            {delta_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_section_header(title: str, icon: str = None):
    """Render a section header."""
    icon_html = render_icon(icon, size=18) if icon else ""
    st.markdown(
        f"""
        <style>
        .section-header {{
            font-size: {FONTS["section_heading"]};
            font-weight: 600;
            color: {COLORS["primary_text"]};
            margin: {SPACING["lg"]} 0 {SPACING["md"]} 0;
            display: flex;
            align-items: center;
            gap: {SPACING["sm"]};
        }}
        </style>
        <div class="section-header">{icon_html} {title}</div>
        """,
        unsafe_allow_html=True,
    )


def render_status_badge(status: str, size: str = "md"):
    """Render a status badge."""
    status_colors = {
        "completed": COLORS["success"],
        "success": COLORS["success"],
        "pending": COLORS["warning"],
        "in_progress": COLORS["warning"],
        "failed": COLORS["error"],
        "error": COLORS["error"],
    }

    bg_color = status_colors.get(status.lower(), COLORS["info"])
    font_size = FONTS["caption"] if size == "sm" else FONTS["metadata"]

    st.markdown(
        f"""
        <style>
        .status-badge {{
            display: inline-block;
            padding: 4px 12px;
            background-color: {bg_color}15;
            color: {bg_color};
            border-radius: {BORDER_RADIUS["sm"]};
            font-size: {font_size};
            font-weight: 500;
            text-transform: capitalize;
        }}
        </style>
        <span class="status-badge">{status.replace("_", " ")}</span>
        """,
        unsafe_allow_html=True,
    )


def render_empty_state(
    title: str,
    message: str,
    icon: str = "folder",
    action_text: str = None,
    action_key: str = None,
):
    """Render a professional empty state."""
    icon_html = render_icon(icon, size=64)

    st.markdown(
        f"""
        <style>
        .empty-state {{
            text-align: center;
            padding: {SPACING["2xl"]} {SPACING["lg"]};
            background-color: {COLORS["card_background"]};
            border: 1px solid {COLORS["border"]};
            border-radius: {BORDER_RADIUS["lg"]};
        }}
        .empty-state-icon {{
            color: {COLORS["muted_text"]};
            margin-bottom: {SPACING["md"]};
        }}
        .empty-state-title {{
            font-size: {FONTS["section_heading"]};
            font-weight: 600;
            color: {COLORS["primary_text"]};
            margin-bottom: {SPACING["sm"]};
        }}
        .empty-state-message {{
            font-size: {FONTS["body_text"]};
            color: {COLORS["secondary_text"]};
            margin-bottom: {SPACING["lg"]};
            max-width: 500px;
            margin-left: auto;
            margin-right: auto;
        }}
        </style>
        <div class="empty-state">
            <div class="empty-state-icon">{icon_html}</div>
            <div class="empty-state-title">{title}</div>
            <div class="empty-state-message">{message}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if action_text and action_key:
        if st.button(action_text, key=action_key, type="primary"):
            return True
    return False


def render_insight_card(
    title: str,
    description: str,
    icon: str,
    value: str = None,
    action_label: str = None,
    action_key: str = None,
):
    """Render an insight card."""
    icon_html = render_icon(icon, size=20)
    value_html = f'<div style="font-size: {FONTS["kpi_value"]}; font-weight: 600; color: {COLORS["primary_text"]}; margin-bottom: {SPACING["xs"]};">{value}</div>' if value else ""

    st.markdown(
        f"""
        <style>
        .insight-card {{
            background-color: {COLORS["card_background"]};
            border: 1px solid {COLORS["border"]};
            border-radius: {BORDER_RADIUS["lg"]};
            padding: {SPACING["md"]};
            box-shadow: {SHADOWS["md"]};
        }}
        .insight-header {{
            display: flex;
            align-items: center;
            gap: {SPACING["sm"]};
            margin-bottom: {SPACING["sm"]};
        }}
        .insight-icon {{
            color: {COLORS["primary_accent"]};
        }}
        .insight-title {{
            font-size: {FONTS["body_text"]};
            font-weight: 600;
            color: {COLORS["primary_text"]};
        }}
        .insight-description {{
            font-size: {FONTS["metadata"]};
            color: {COLORS["secondary_text"]};
            margin-bottom: {SPACING["md"]};
        }}
        </style>
        <div class="insight-card">
            <div class="insight-header">
                <div class="insight-icon">{icon_html}</div>
                <div class="insight-title">{title}</div>
            </div>
            {value_html}
            <div class="insight-description">{description}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if action_label and action_key:
        if st.button(action_label, key=action_key, width="stretch"):
            return True
    return False


def render_card(content: str | None = None, title: str = None, icon: str = None):
    """Render a generic card container."""
    icon_html = render_icon(icon, size=18) if icon else ""

    st.markdown(
        f"""
        <style>
        .generic-card {{
            background-color: {COLORS["card_background"]};
            border: 1px solid {COLORS["border"]};
            border-radius: {BORDER_RADIUS["lg"]};
            padding: {SPACING["md"]};
            box-shadow: {SHADOWS["md"]};
            margin-bottom: {SPACING["md"]};
        }}
        .card-header {{
            display: flex;
            align-items: center;
            gap: {SPACING["sm"]};
            margin-bottom: {SPACING["md"]};
        }}
        .card-title {{
            font-size: {FONTS["section_heading"]};
            font-weight: 600;
            color: {COLORS["primary_text"]};
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    if title:
        st.markdown(
            f'<div class="card-header"><div class="card-icon">{icon_html}</div><div class="card-title">{title}</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div class="generic-card">', unsafe_allow_html=True)
    if content:
        st.markdown(content, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


def render_action_card(
    title: str,
    description: str,
    icon: str,
    value: str = None,
    action_label: str = None,
    action_key: str = None,
):
    """Render an action card with right arrow."""
    icon_html = render_icon(icon, size=20)
    arrow_html = render_icon("chevron_right", size=16)
    value_html = f'<div style="font-size: {FONTS["kpi_value"]}; font-weight: 600; color: {COLORS["primary_text"]}; margin-bottom: {SPACING["xs"]};">{value}</div>' if value else ""

    st.markdown(
        f"""
        <style>
        .action-card {{
            background-color: {COLORS["card_background"]};
            border: 1px solid {COLORS["border"]};
            border-radius: {BORDER_RADIUS["lg"]};
            padding: {SPACING["md"]};
            box-shadow: {SHADOWS["md"]};
            cursor: pointer;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}
        .action-card:hover {{
            box-shadow: {SHADOWS["lg"]};
            transform: translateY(-2px);
            border-color: {COLORS["primary_accent"]};
        }}
        .action-content {{
            display: flex;
            align-items: center;
            gap: {SPACING["md"]};
        }}
        .action-icon {{
            color: {COLORS["primary_accent"]};
        }}
        .action-title {{
            font-size: {FONTS["body_text"]};
            font-weight: 600;
            color: {COLORS["primary_text"]};
        }}
        .action-description {{
            font-size: {FONTS["metadata"]};
            color: {COLORS["secondary_text"]};
        }}
        .action-arrow {{
            color: {COLORS["muted_text"]};
        }}
        </style>
        <div class="action-card">
            <div class="action-content">
                <div class="action-icon">{icon_html}</div>
                <div>
                    {value_html}
                    <div class="action-title">{title}</div>
                    <div class="action-description">{description}</div>
                </div>
            </div>
            <div class="action-arrow">{arrow_html}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if action_label and action_key:
        if st.button(action_label, key=action_key, width="stretch"):
            return True
    return False
