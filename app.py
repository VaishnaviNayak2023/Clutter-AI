"""ClutterAI - Main Streamlit Application."""

import streamlit as st

from src.ai_clutter_cleaner.database import init_database
from src.ai_clutter_cleaner.logging_config import setup_logging
from src.ai_clutter_cleaner.ui import init_page_state, render_sidebar
from src.ai_clutter_cleaner.ui.theme import css_variables

# Configure page
st.set_page_config(
    page_title="ClutterAI",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load custom CSS after Streamlit page configuration.
with open(".streamlit/style.css", encoding="utf-8") as f:
    st.markdown(
        f"<style>{css_variables()}\n{f.read()}</style>",
        unsafe_allow_html=True,
    )

# Setup logging
setup_logging()

# Initialize page state
init_page_state()

# Initialize database on first run
if "db_initialized" not in st.session_state:
    try:
        init_database()
        st.session_state["db_initialized"] = True
    except Exception as e:
        st.error(f"Failed to initialize database: {e}")
        st.session_state["db_initialized"] = False

# Render the shared navigation shell
render_sidebar()

# Page routing
current_page = st.session_state.get("current_page", "Dashboard")

if current_page == "Dashboard":
    from pages.dashboard import render_dashboard
    render_dashboard()
elif current_page == "Scan_Files":
    from pages.scan_files import render_scan_files
    render_scan_files()
elif current_page == "AI_Organization":
    from pages.ai_organization import render_ai_organization
    render_ai_organization()
elif current_page == "Duplicate_Finder":
    from pages.duplicate_finder import render_duplicate_finder
    render_duplicate_finder()
elif current_page == "Search_Explorer":
    from pages.search_explorer import render_search_explorer
    render_search_explorer()
elif current_page == "History":
    from pages.history import render_history
    render_history()
elif current_page == "Reports":
    from pages.reports import render_reports
    render_reports()
elif current_page == "Settings":
    from pages.settings import render_settings
    render_settings()
else:
    st.error("Page not found")
