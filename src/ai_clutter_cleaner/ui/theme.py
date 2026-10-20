"""Central design tokens for the ClutterAI interface."""

COLORS = {
    "app_background": "#F7F5EE",
    "sidebar_background": "#FCFBF7",
    "card_background": "#FFFFFF",
    "secondary_surface": "#FAF8F2",
    "elevated_surface": "#FFFFFF",
    "primary_text": "#252B33",
    "secondary_text": "#68717D",
    "muted_text": "#68717D",
    "brand": "#D5A333",
    "primary_accent": "#8A5B0B",
    "accent_hover": "#C18B20",
    "accent_light": "#FBF2DC",
    "primary_action_text": "#FFFFFF",
    "primary_action_hover_text": "#FFFFFF",
    "border": "#E9E5DA",
    "border_light": "#F1EEE6",
    "control_border": "#DDD9CE",
    "focus_ring": "#8D6518",
    "link": "#80580D",
    "success": "#247A59",
    "success_surface": "#E8F4EE",
    "warning": "#875B0C",
    "warning_surface": "#FBF2DF",
    "error": "#B54747",
    "error_surface": "#F9EAEA",
    "info": "#28659B",
    "info_surface": "#EAF2FA",
    "disabled_text": "#68717D",
    "selected_surface": "#F8F1DF",
    "overlay": "rgba(37, 43, 51, 0.48)",
}

CHART_COLORS = (
    "#D5A333",
    "#8E9294",
    "#A89567",
    "#7CA0C4",
    "#AB8AD0",
    "#D88376",
    "#74A99D",
    "#D3D2CC",
)

# Typography
FONTS = {
    "family": "Inter, 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif",
    "page_heading": "29px",
    "section_heading": "16px",
    "card_heading": "16px",
    "kpi_value": "28px",
    "body_text": "14px",
    "metadata": "12px",
    "caption": "12px",
}

# Spacing scale (4px base)
SPACING = {
    "xs": "4px",
    "sm": "8px",
    "md": "16px",
    "lg": "24px",
    "xl": "32px",
    "2xl": "48px",
}

# Border radius
BORDER_RADIUS = {
    "sm": "6px",
    "md": "8px",
    "lg": "12px",
    "xl": "16px",
}

# Shadow
SHADOWS = {
    "sm": "0 1px 2px rgba(0, 0, 0, 0.05)",
    "md": "0 2px 8px rgba(0, 0, 0, 0.04)",
    "lg": "0 4px 16px rgba(0, 0, 0, 0.08)",
}


def css_variables() -> str:
    """Serialize the shared tokens for use by the global stylesheet."""
    groups = {
        "color": COLORS,
        "font": FONTS,
        "space": SPACING,
        "radius": BORDER_RADIUS,
        "shadow": SHADOWS,
    }
    declarations = [
        f"--{prefix}-{name.replace('_', '-')}: {value};"
        for prefix, tokens in groups.items()
        for name, value in tokens.items()
    ]
    declarations.extend(
        f"--chart-{index}: {value};" for index, value in enumerate(CHART_COLORS, start=1)
    )
    return ":root {\n" + "\n".join(declarations) + "\n}"
