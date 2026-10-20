"""UI components package for ClutterAI dashboard."""

from .components import render_icon
from .layout import (
    init_page_state,
    navigate_to_page,
    render_global_header,
    render_sidebar,
)
from .presentation import (
    render_action_card,
    render_empty_state,
    render_insight_card,
    render_kpi_card,
    render_page_header,
    render_section_header,
    render_status_badge,
)

__all__ = [
    "render_icon",
    "render_kpi_card",
    "render_page_header",
    "render_section_header",
    "render_status_badge",
    "render_empty_state",
    "render_insight_card",
    "render_action_card",
    "render_sidebar",
    "render_global_header",
    "init_page_state",
    "navigate_to_page",
]
