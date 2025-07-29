#!/usr/bin/env python3
"""
Do You NPC - Main Streamlit Application

This is the main UI application for the Do You NPC project, providing
an easy-to-use interface for testing and interacting with the system.
"""

import streamlit as st


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
            ["Home", "Personas", "Prompts", "Tags"],
            index=0
        )
    
    # Main content area
    if selected_tab == "Home":
        show_home_page()
    elif selected_tab == "Personas":
        show_personas_page()
    elif selected_tab == "Prompts":
        show_prompts_page()
    elif selected_tab == "Tags":
        show_tags_page()


def show_home_page():
    """Display the home/splash screen."""
    st.title("🎲 Welcome to Do You NPC!")
    
    st.markdown("""
    ## Your AI-Powered NPC Generation System
    
    Welcome to **Do You NPC**, a powerful tool for creating dynamic and engaging 
    non-player characters for your tabletop RPGs, video games, or creative writing projects.
    
    ### What You Can Do Here:
    
    🎭 **Personas** - Create and manage character personalities, backgrounds, and traits
    
    📝 **Prompts** - Design and test prompt templates for character generation
    
    🏷️ **Tags** - Organize and categorize your NPCs with custom tags
    
    ### Getting Started
    
    Use the navigation panel on the left to explore the different sections of the application.
    This is an early prototype, so features are being actively developed!
    
    ---
    
    *Built with ❤️ for tabletop enthusiasts and game masters everywhere.*
    """)
    
    # Project status section
    st.subheader("🚧 Project Status")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Version", "0.1.0", "Alpha")
    
    with col2:
        st.metric("Features", "3", "In Development")
    
    with col3:
        st.metric("Status", "Active", "Prototyping")


def show_personas_page():
    """Display the personas management page."""
    st.title("🎭 Personas")
    st.info("👷 This section is under construction. Character persona management will be available soon!")
    
    st.markdown("""
    ### Coming Soon:
    - Create new character personas
    - Edit existing personas
    - Manage personality traits and backgrounds
    - Preview generated characters
    """)


def show_prompts_page():
    """Display the prompts management page."""
    st.title("📝 Prompts")
    st.info("👷 This section is under construction. Prompt template management will be available soon!")
    
    st.markdown("""
    ### Coming Soon:
    - Create custom prompt templates
    - Test prompt effectiveness
    - Manage prompt parameters
    - Preview generated content
    """)


def show_tags_page():
    """Display the tags management page."""
    st.title("🏷️ Tags")
    st.info("👷 This section is under construction. Tag management will be available soon!")
    
    st.markdown("""
    ### Coming Soon:
    - Create and organize tags
    - Assign tags to NPCs
    - Filter content by tags
    - Manage tag hierarchies
    """)


if __name__ == "__main__":
    main()