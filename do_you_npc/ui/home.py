"""
Home page UI component for Do You NPC application.
"""

import streamlit as st


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