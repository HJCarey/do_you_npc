"""
Tags page UI component for Do You NPC application.
"""

import streamlit as st
from typing import Dict, List, Optional

from do_you_npc.ui.api_client import get_api_client


def show_tags_page():
    """Display the tags management page."""
    st.title("🏷️ Tags")
    
    api_client = get_api_client()
    
    # Check API health
    if not api_client.health_check():
        st.error("⚠️ Cannot connect to API server. Please make sure the FastAPI server is running.")
        st.code("uvicorn do_you_npc.api.main:app --host 0.0.0.0 --port 8000 --reload")
        return
    
    # Load campaigns and tags
    campaigns = api_client.get_campaigns()
    all_tags = api_client.get_tags()
    
    if not all_tags:
        st.warning("No tags found in the system.")
        return
    
    # Campaign filter
    st.subheader("Filter by Campaign")
    
    # Create campaign options with "All" as first option
    campaign_options = {"All Tags": None}
    if campaigns:
        campaign_options.update({f"{camp['name']} (ID: {camp['id']})": camp['id'] 
                               for camp in campaigns})
    
    selected_campaign_key = st.selectbox(
        "Choose a campaign to filter tags, or view all:",
        options=list(campaign_options.keys()),
        index=0
    )
    
    selected_campaign_id = campaign_options[selected_campaign_key]
    
    st.markdown("---")
    
    # Filter tags based on campaign selection
    if selected_campaign_id is None:
        # Show all tags
        filtered_tags = all_tags
        st.subheader("All Tags")
        st.write(f"Showing all {len(filtered_tags)} tags in the system:")
    else:
        # Filter tags used in the selected campaign
        personas = api_client.get_personas(campaign_id=selected_campaign_id)
        campaign_tag_ids = set()
        
        if personas:
            for persona in personas:
                if persona.get('tags'):
                    for tag in persona['tags']:
                        campaign_tag_ids.add(tag['id'])
        
        filtered_tags = [tag for tag in all_tags if tag['id'] in campaign_tag_ids]
        
        # Find campaign name for display
        selected_campaign = next((camp for camp in campaigns if camp['id'] == selected_campaign_id), None)
        campaign_name = selected_campaign['name'] if selected_campaign else "Unknown"
        
        st.subheader(f"Tags used in {campaign_name}")
        
        if not filtered_tags:
            st.info(f"No tags are currently used by personas in the '{campaign_name}' campaign.")
            return
        
        st.write(f"Found {len(filtered_tags)} tag(s) used in this campaign:")
    
    # Display tags
    for tag in filtered_tags:
        display_tag_card(tag)


def display_tag_card(tag: Dict):
    """Display a single tag as an expandable card."""
    
    # Create a unique key for the expander
    expander_key = f"tag_{tag['id']}"
    
    # Tag header with name and emoji
    tag_header = f"🏷️ **{tag['name']}**"
    
    with st.expander(tag_header, expanded=False):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown("### 📖 Tag Content")
            
            # Display tag text in a scrollable text area
            if tag.get('text_body'):
                st.text_area(
                    label="",
                    value=tag['text_body'],
                    height=300,
                    disabled=True,
                    key=f"content_{tag['id']}"
                )
            else:
                st.write("*No content available for this tag.*")
        
        with col2:
            st.markdown("### ℹ️ Details")
            st.write(f"**ID:** {tag['id']}")
            st.write(f"**Created:** {tag['created_at'][:10] if tag.get('created_at') else 'Unknown'}")
            
            # Future action buttons (placeholder for future functionality)
            st.markdown("---")
            if st.button(f"✏️ Edit", key=f"edit_{tag['id']}", disabled=True):
                # TODO: Implement edit functionality
                pass
            
            if st.button(f"🗑️ Delete", key=f"delete_{tag['id']}", disabled=True):
                # TODO: Implement delete functionality
                pass