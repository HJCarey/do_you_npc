"""
Personas page UI component for Do You NPC application.
"""

import streamlit as st
from typing import Dict, List, Optional

from do_you_npc.ui.api_client import get_api_client


def show_personas_page():
    """Display the personas management page."""
    st.title("🎭 Personas")
    
    api_client = get_api_client()
    
    # Check API health
    if not api_client.health_check():
        st.error("⚠️ Cannot connect to API server. Please make sure the FastAPI server is running.")
        st.code("uvicorn do_you_npc.api.main:app --host 0.0.0.0 --port 8000 --reload")
        return
    
    # Load campaigns for dropdown
    campaigns = api_client.get_campaigns()
    if not campaigns:
        st.warning("No campaigns found. Please create a campaign first.")
        return
    
    # Campaign selector
    st.subheader("Select Campaign")
    campaign_options = {f"{camp['name']} (ID: {camp['id']})": camp['id'] 
                       for camp in campaigns}
    
    selected_campaign_key = st.selectbox(
        "Choose a campaign to view personas:",
        options=list(campaign_options.keys()),
        index=0
    )
    
    selected_campaign_id = campaign_options[selected_campaign_key]
    
    # Find the selected campaign details
    selected_campaign = next(camp for camp in campaigns if camp['id'] == selected_campaign_id)
    
    # Display campaign info
    with st.expander("📋 Campaign Details", expanded=False):
        st.write(f"**Name:** {selected_campaign['name']}")
        if selected_campaign.get('description'):
            st.write(f"**Description:** {selected_campaign['description']}")
        st.write(f"**Created:** {selected_campaign['created_at'][:10]}")
    
    st.markdown("---")
    
    # Load personas for selected campaign
    st.subheader(f"Personas in {selected_campaign['name']}")
    
    personas = api_client.get_personas(campaign_id=selected_campaign_id)
    
    if not personas:
        st.info("No personas found in this campaign.")
        
        # TODO: Add create persona form here in future
        st.markdown("*Persona creation form coming soon...*")
        return
    
    # Display personas
    st.write(f"Found {len(personas)} persona(s) in this campaign:")
    
    for persona in personas:
        display_persona_card(persona)


def display_persona_card(persona: Dict):
    """Display a single persona as an expandable card."""
    
    # Create a unique key for the expander
    expander_key = f"persona_{persona['id']}"
    
    # Persona header with name and basic info
    persona_header = f"🎭 **{persona['name']}**"
    
    with st.expander(persona_header, expanded=False):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### 📖 Backstory")
            st.write(persona['backstory'])
            
            st.markdown("### 🧠 Personality")
            st.write(persona['personality'])
        
        with col2:
            st.markdown("### ℹ️ Details")
            st.write(f"**ID:** {persona['id']}")
            st.write(f"**Campaign:** {persona['campaign']['name']}")
            st.write(f"**Created:** {persona['created_at'][:10]}")
            
            # Display tags
            if persona.get('tags'):
                st.markdown("### 🏷️ Tags")
                for tag in persona['tags']:
                    st.markdown(f"- **{tag['name']}**: {tag['text_body']}")
            else:
                st.markdown("### 🏷️ Tags")
                st.write("*No tags assigned*")
        
        # Action buttons (placeholder for future functionality)
        st.markdown("---")
        col_edit, col_delete = st.columns(2)
        
        with col_edit:
            if st.button(f"✏️ Edit", key=f"edit_{persona['id']}", disabled=True):
                # TODO: Implement edit functionality
                pass
        
        with col_delete:
            if st.button(f"🗑️ Delete", key=f"delete_{persona['id']}", disabled=True):
                # TODO: Implement delete functionality
                pass