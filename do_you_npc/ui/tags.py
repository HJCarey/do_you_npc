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
    
    # Initialize session state for UI management
    if 'show_create_tag' not in st.session_state:
        st.session_state.show_create_tag = False
    if 'editing_tag_id' not in st.session_state:
        st.session_state.editing_tag_id = None
    if 'tag_to_delete' not in st.session_state:
        st.session_state.tag_to_delete = None
    
    # Create tag section
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("➕ Create New Tag", type="primary"):
            st.session_state.show_create_tag = True
            st.session_state.editing_tag_id = None
    
    if st.session_state.show_create_tag:
        show_create_tag_form(api_client)
        st.markdown("---")
    
    # Load campaigns and tags
    campaigns = api_client.get_campaigns()
    all_tags = api_client.get_tags()
    
    if not all_tags:
        st.warning("No tags found in the system.")
        if not st.session_state.show_create_tag:
            st.info("👆 Click 'Create New Tag' above to add your first tag!")
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
    
    # Handle delete confirmation
    if st.session_state.tag_to_delete:
        show_delete_confirmation(api_client, st.session_state.tag_to_delete)
    
    # Display tags
    for tag in filtered_tags:
        display_tag_card(tag, api_client)


def display_tag_card(tag: Dict, api_client):
    """Display a single tag as an expandable card."""
    
    # Create a unique key for the expander
    expander_key = f"tag_{tag['id']}"
    
    # Tag header with name and emoji
    tag_header = f"🏷️ **{tag['name']}**"
    
    # Check if this tag is being edited
    is_editing = st.session_state.editing_tag_id == tag['id']
    
    with st.expander(tag_header, expanded=is_editing):
        if is_editing:
            # Show edit form
            show_edit_tag_form(api_client, tag)
        else:
            # Show read-only view
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown("### 📖 Tag Content")
                
                # Display tag text in a scrollable text area
                if tag.get('text_body'):
                    st.text_area(
                        label="Tag Content",
                        value=tag['text_body'],
                        height=300,
                        disabled=True,
                        key=f"content_{tag['id']}",
                        label_visibility="collapsed"
                    )
                else:
                    st.write("*No content available for this tag.*")
            
            with col2:
                st.markdown("### ℹ️ Details")
                st.write(f"**ID:** {tag['id']}")
                st.write(f"**Created:** {tag['created_at'][:10] if tag.get('created_at') else 'Unknown'}")
                
                # Action buttons
                st.markdown("---")
                if st.button(f"✏️ Edit", key=f"edit_{tag['id']}"):
                    st.session_state.editing_tag_id = tag['id']
                    st.session_state.show_create_tag = False
                    st.rerun()
                
                if st.button(f"🗑️ Delete", key=f"delete_{tag['id']}"):
                    st.session_state.tag_to_delete = tag
                    st.rerun()


def show_create_tag_form(api_client):
    """Display the create tag form."""
    st.subheader("➕ Create New Tag")
    
    with st.form("create_tag_form"):
        col1, col2 = st.columns([1, 1])
        
        with col1:
            tag_name = st.text_input(
                "Tag Name*",
                placeholder="Enter tag name (e.g., 'Merchant', 'Noble', 'Warrior')"
            )
        
        with col2:
            # Just a spacer for now
            st.write("")
        
        tag_content = st.text_area(
            "Tag Content",
            placeholder="Enter detailed description, traits, or context for this tag...",
            height=200,
            help="Describe what this tag represents, typical characteristics, or usage notes."
        )
        
        col1, col2, _ = st.columns([1, 1, 3])
        
        with col1:
            submit_button = st.form_submit_button("✅ Create Tag", type="primary")
        
        with col2:
            cancel_button = st.form_submit_button("❌ Cancel")
        
        if cancel_button:
            st.session_state.show_create_tag = False
            st.rerun()
        
        if submit_button:
            if not tag_name.strip():
                st.error("Tag name is required!")
                return
            
            try:
                tag_data = {
                    "name": tag_name.strip(),
                    "text_body": tag_content.strip() if tag_content.strip() else None
                }
                
                new_tag = api_client.create_tag(tag_data)
                st.success(f"✅ Tag '{new_tag['name']}' created successfully!")
                st.session_state.show_create_tag = False
                st.rerun()
                
            except Exception as e:
                st.error(f"Error creating tag: {str(e)}")


def show_edit_tag_form(api_client, tag: Dict):
    """Display the edit tag form."""
    st.markdown("### ✏️ Edit Tag")
    
    with st.form(f"edit_tag_form_{tag['id']}"):
        col1, col2 = st.columns([1, 1])
        
        with col1:
            tag_name = st.text_input(
                "Tag Name*",
                value=tag['name'],
                placeholder="Enter tag name"
            )
        
        with col2:
            # Just a spacer for now
            st.write("")
        
        tag_content = st.text_area(
            "Tag Content",
            value=tag.get('text_body', ''),
            placeholder="Enter detailed description, traits, or context for this tag...",
            height=200,
            help="Describe what this tag represents, typical characteristics, or usage notes."
        )
        
        col1, col2, _ = st.columns([1, 1, 3])
        
        with col1:
            submit_button = st.form_submit_button("✅ Save Changes", type="primary")
        
        with col2:
            cancel_button = st.form_submit_button("❌ Cancel")
        
        if cancel_button:
            st.session_state.editing_tag_id = None
            st.rerun()
        
        if submit_button:
            if not tag_name.strip():
                st.error("Tag name is required!")
                return
            
            try:
                tag_data = {
                    "name": tag_name.strip(),
                    "text_body": tag_content.strip() if tag_content.strip() else None
                }
                
                updated_tag = api_client.update_tag(tag['id'], tag_data)
                st.success(f"✅ Tag '{updated_tag['name']}' updated successfully!")
                st.session_state.editing_tag_id = None
                st.rerun()
                
            except Exception as e:
                st.error(f"Error updating tag: {str(e)}")


def show_delete_confirmation(api_client, tag: Dict):
    """Display delete confirmation dialog."""
    st.error(f"🗑️ **Delete Tag: {tag['name']}**")
    st.warning("⚠️ **Warning:** This action cannot be undone. The tag will be removed from all personas that use it.")
    
    col1, col2, _ = st.columns([1, 1, 3])
    
    with col1:
        if st.button("🗑️ Confirm Delete", type="primary"):
            try:
                api_client.delete_tag(tag['id'])
                st.success(f"✅ Tag '{tag['name']}' deleted successfully!")
                st.session_state.tag_to_delete = None
                st.rerun()
            except Exception as e:
                st.error(f"Error deleting tag: {str(e)}")
    
    with col2:
        if st.button("❌ Cancel"):
            st.session_state.tag_to_delete = None
            st.rerun()