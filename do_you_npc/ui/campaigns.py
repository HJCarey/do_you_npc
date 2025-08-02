"""
Campaigns page UI component for Do You NPC application.
"""

import streamlit as st
from typing import Dict, List, Optional

from do_you_npc.ui.api_client import get_api_client


def show_campaigns_page():
    """Display the campaigns management page."""
    st.title("🗺️ Campaigns")
    
    api_client = get_api_client()
    
    # Check API health
    if not api_client.health_check():
        st.error("⚠️ Cannot connect to API server. Please make sure the FastAPI server is running.")
        st.code("uvicorn do_you_npc.api.main:app --host 0.0.0.0 --port 8000 --reload")
        return
    
    # Check if we should show a success message after campaign creation
    if st.session_state.get("campaign_created_success", False):
        campaign_name = st.session_state.get("campaign_created_name", "")
        st.success(f"✅ Campaign '{campaign_name}' created successfully!")

        st.session_state["campaign_created_success"] = False
        if "campaign_created_name" in st.session_state:
            del st.session_state["campaign_created_name"]
    
    # Create two tabs: View Campaigns and Create New Campaign
    tab1, tab2 = st.tabs(["📋 View Campaigns", "➕ Create New Campaign"])
    
    with tab1:
        show_campaigns_list(api_client)
    
    with tab2:
        show_create_campaign_form(api_client)


def show_campaigns_list(api_client):
    """Display the list of all campaigns."""
    st.subheader("All Campaigns")
    
    # Load campaigns
    campaigns = api_client.get_campaigns()
    
    # Clean up deleted campaign flags for campaigns that no longer exist
    if campaigns:
        current_campaign_ids = {campaign['id'] for campaign in campaigns}
        # Remove deleted flags for campaigns that are no longer in the list
        keys_to_remove = []
        for key in st.session_state:
            if key.startswith("campaign_deleted_"):
                campaign_id = int(key.split("_")[-1])
                if campaign_id not in current_campaign_ids:
                    keys_to_remove.append(key)
        
        for key in keys_to_remove:
            del st.session_state[key]
    
    if not campaigns:
        st.info("No campaigns found. Create your first campaign using the 'Create New Campaign' tab!")
        return
    
    # Filter out campaigns that are marked as deleted in this session
    visible_campaigns = [
        campaign for campaign in campaigns 
        if not st.session_state.get(f"campaign_deleted_{campaign['id']}", False)
    ]
    
    if not visible_campaigns:
        st.info("No campaigns to display.")
        return
    
    st.write(f"Found {len(visible_campaigns)} campaign(s):")
    
    # Display campaigns
    for campaign in visible_campaigns:
        display_campaign_card(campaign, api_client)


def show_create_campaign_form(api_client):
    """Display the form to create a new campaign."""
    st.subheader("Create New Campaign")
    
    # Initialize form values from session state or defaults
    if "new_campaign_name" not in st.session_state:
        st.session_state["new_campaign_name"] = ""
    if "new_campaign_description" not in st.session_state:
        st.session_state["new_campaign_description"] = ""
    
    with st.form("create_campaign_form"):
        st.markdown("### Campaign Details")
        
        # Campaign name input
        name = st.text_input(
            "Campaign Name *",
            value=st.session_state["new_campaign_name"],
            placeholder="Enter campaign name (e.g., 'The Dragon's Quest')",
            help="Choose a unique name for your campaign"
        )
        
        # Campaign description input
        description = st.text_area(
            "Campaign Description",
            value=st.session_state["new_campaign_description"],
            placeholder="Describe your campaign setting, theme, or story...",
            help="Optional description to help organize your campaigns",
            height=150
        )

        def clear_inputs():
            st.session_state["new_campaign_name"] = ""
            st.session_state["new_campaign_description"] = ""
            print("called clear_inputs()")
        
        # Submit button
        submitted = st.form_submit_button("🗺️ Create Campaign", type="primary",
                                          on_click=clear_inputs)
        
        if submitted:
            if not name.strip():
                st.error("Campaign name is required!")
                return
            
            # Create the campaign
            with st.spinner("Creating campaign..."):
                result = api_client.create_campaign(
                    name=name.strip(),
                    description=description.strip() if description.strip() else None
                )
            
            if result:
                # Clear the form fields and set success flag
                clear_inputs()
                st.session_state["campaign_created_success"] = True
                st.session_state["campaign_created_name"] = name
                print('entered result conditional in campaigns')
                st.rerun()
            else:
                st.error("Failed to create campaign. The name might already exist.")


def display_campaign_card(campaign: Dict, api_client):
    """Display a single campaign as an expandable card."""
    
    # Check if this campaign is being edited
    is_editing = st.session_state.get(f"editing_campaign_{campaign['id']}", False)
    is_deleting = st.session_state.get(f"deleting_campaign_{campaign['id']}", False)
    
    # Campaign header with name and emoji
    if is_editing:
        campaign_header = f"✏️ **Editing: {campaign['name']}**"
        expanded = True
    elif is_deleting:
        campaign_header = f"🗑️ **Delete: {campaign['name']}**"
        expanded = True
    else:
        campaign_header = f"🗺️ **{campaign['name']}**"
        expanded = False
    
    with st.expander(campaign_header, expanded=expanded):
        if is_editing:
            # Show inline edit form
            show_inline_edit_form(campaign, api_client)
        elif is_deleting:
            # Show inline delete confirmation
            show_inline_delete_confirmation(campaign, api_client)
        else:
            # Show normal campaign view
            show_campaign_details(campaign, api_client)


def show_campaign_details(campaign: Dict, api_client):
    """Show the normal campaign details view."""
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📖 Description")
        if campaign.get('description'):
            st.write(campaign['description'])
        else:
            st.write("*No description provided*")
        
        # Load and display persona count for this campaign
        personas = api_client.get_personas(campaign_id=campaign['id'])
        persona_count = len(personas) if personas else 0
        
        st.markdown("### 🎭 Campaign Content")
        st.write(f"**Personas:** {persona_count}")
        
        if personas:
            st.markdown("**Persona List:**")
            for persona in personas[:5]:  # Show first 5 personas
                st.write(f"• {persona['name']}")
            
            if len(personas) > 5:
                st.write(f"• ... and {len(personas) - 5} more")
    
    with col2:
        st.markdown("### ℹ️ Details")
        st.write(f"**ID:** {campaign['id']}")
        st.write(f"**Created:** {campaign['created_at'][:10]}")
        if campaign.get('updated_at') and campaign['updated_at'] != campaign['created_at']:
            st.write(f"**Updated:** {campaign['updated_at'][:10]}")
        
        # Action buttons
        st.markdown("---")
        if st.button(f"✏️ Edit", key=f"edit_{campaign['id']}"):
            st.session_state[f"editing_campaign_{campaign['id']}"] = True
            st.rerun()
        
        if st.button(f"🗑️ Delete", key=f"delete_{campaign['id']}"):
            st.session_state[f"deleting_campaign_{campaign['id']}"] = True
            st.rerun()
        
        st.markdown("---")
        if st.button(f"👥 View Personas", key=f"personas_{campaign['id']}", disabled=True):
            # TODO: Navigate to personas page filtered by this campaign
            pass


def show_inline_edit_form(campaign: Dict, api_client):
    """Show the inline edit form within the campaign card."""
    with st.form(f"edit_campaign_form_{campaign['id']}"):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### ✏️ Edit Campaign Details")
            
            # Pre-populate with current values
            new_name = st.text_input(
                "Campaign Name *",
                value=campaign['name'],
                placeholder="Enter campaign name",
                help="Choose a unique name for your campaign"
            )
            
            new_description = st.text_area(
                "Campaign Description",
                value=campaign.get('description', ''),
                placeholder="Describe your campaign setting, theme, or story...",
                help="Optional description to help organize your campaigns",
                height=150
            )
        
        with col2:
            st.markdown("### 💾 Save Changes")
            st.write("Review your changes and save them, or cancel to go back.")
            
            st.markdown("---")
            
            if st.form_submit_button("💾 Save Changes", type="primary", use_container_width=True):
                if not new_name.strip():
                    st.error("Campaign name is required!")
                    return
                
                with st.spinner("Updating campaign..."):
                    result = api_client.update_campaign(
                        campaign_id=campaign['id'],
                        name=new_name.strip(),
                        description=new_description.strip() if new_description.strip() else None
                    )
                
                if result:
                    st.success(f"✅ Campaign '{new_name}' updated successfully!")
                    st.session_state[f"editing_campaign_{campaign['id']}"] = False
                    st.rerun()
                else:
                    st.error("Failed to update campaign. The name might already exist.")
            
            if st.form_submit_button("❌ Cancel", use_container_width=True):
                st.session_state[f"editing_campaign_{campaign['id']}"] = False
                st.rerun()


def show_inline_delete_confirmation(campaign: Dict, api_client):
    """Show the inline delete confirmation within the campaign card."""
    # Load personas to check if campaign has any
    personas = api_client.get_personas(campaign_id=campaign['id'])
    persona_count = len(personas) if personas else 0
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if persona_count > 0:
            st.error(f"⚠️ This campaign contains {persona_count} persona(s). You cannot delete a campaign that contains personas.")
            st.markdown("**Personas in this campaign:**")
            for persona in personas[:10]:  # Show first 10
                st.write(f"• {persona['name']}")
            if len(personas) > 10:
                st.write(f"• ... and {len(personas) - 10} more")
        else:
            st.warning(f"⚠️ **Are you sure you want to delete the campaign '{campaign['name']}'?**")
            st.write("This action cannot be undone.")
            
            if campaign.get('description'):
                st.markdown("**Campaign Description:**")
                st.write(campaign['description'])
    
    with col2:
        st.markdown("### 🗑️ Confirm Deletion")
        
        if persona_count > 0:
            st.write("Delete the personas first, then you can delete this campaign.")
            st.markdown("---")
            if st.button("❌ Cancel", key=f"cancel_delete_{campaign['id']}", use_container_width=True):
                st.session_state[f"deleting_campaign_{campaign['id']}"] = False
                st.rerun()
        else:
            st.write("This will permanently delete the campaign.")
            st.markdown("---")
            
            if st.button("🗑️ Yes, Delete", key=f"confirm_delete_{campaign['id']}", type="primary", use_container_width=True):
                with st.spinner("Deleting campaign..."):
                    # Clear any previous error states
                    if f"delete_error_{campaign['id']}" in st.session_state:
                        del st.session_state[f"delete_error_{campaign['id']}"]
                    
                    success = api_client.delete_campaign(campaign['id'])
                
                if success:
                    # Clear the state and add a flag to indicate successful deletion
                    st.session_state[f"deleting_campaign_{campaign['id']}"] = False
                    st.session_state[f"campaign_deleted_{campaign['id']}"] = True
                    # Show success message and immediately trigger refresh
                    st.success(f"✅ Campaign '{campaign['name']}' deleted successfully!")
                    st.rerun()
                else:
                    # Store error state instead of showing it immediately
                    st.session_state[f"delete_error_{campaign['id']}"] = True
                    st.error("Failed to delete campaign. Please try again.")
            
            if st.button("❌ Cancel", key=f"cancel_delete_{campaign['id']}", use_container_width=True):
                st.session_state[f"deleting_campaign_{campaign['id']}"] = False
                st.rerun()


