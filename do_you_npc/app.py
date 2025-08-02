#!/usr/bin/env python3
"""
Do You NPC - Main Streamlit Application

This is the main UI application for the Do You NPC project, providing
an easy-to-use interface for testing and interacting with the system.
"""

import streamlit as st

from do_you_npc.ui.home import show_home_page
from do_you_npc.ui.campaigns import show_campaigns_page
from do_you_npc.ui.personas import show_personas_page
from do_you_npc.ui.prompts import show_prompts_page
from do_you_npc.ui.tags import show_tags_page


def main():
    """Main application entry point."""
    st.set_page_config(
        page_title="Do You NPC",
        page_icon="🎲",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Sidebar navigation
    with st.sidebar:
        st.title("🎲 Do You NPC")
        st.markdown("---")
        
        # Navigation tabs
        selected_tab = st.radio(
            "Navigation",
            ["Home", "Campaigns", "Personas", "Prompts", "Tags"],
            index=0
        )
    
    # Main content area
    if selected_tab == "Home":
        show_home_page()
    elif selected_tab == "Campaigns":
        show_campaigns_page()
    elif selected_tab == "Personas":
        show_personas_page()
    elif selected_tab == "Prompts":
        show_prompts_page()
    elif selected_tab == "Tags":
        show_tags_page()




if __name__ == "__main__":
    main()