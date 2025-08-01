"""API client for Streamlit UI to communicate with FastAPI backend."""

import requests
from typing import Dict, List, Optional
import streamlit as st


class APIClient:
    """Client for interacting with the Do You NPC API."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """Initialize API client.
        
        Args:
            base_url: Base URL of the FastAPI server
        """
        self.base_url = base_url
        self.session = requests.Session()
    
    def _handle_response(self, response: requests.Response):
        """Handle API response and show errors in Streamlit if needed."""
        if response.status_code >= 400:
            try:
                error_detail = response.json().get("detail", "Unknown error")
            except:
                error_detail = f"HTTP {response.status_code}: {response.text}"
            st.error(f"API Error: {error_detail}")
            return None
        
        try:
            return response.json()
        except:
            return None
    
    # Campaign endpoints
    def get_campaigns(self) -> Optional[List[Dict]]:
        """Get all campaigns."""
        try:
            response = self.session.get(f"{self.base_url}/api/v1/campaigns/")
            return self._handle_response(response)
        except requests.RequestException as e:
            st.error(f"Failed to connect to API: {e}")
            return None
    
    def get_campaign(self, campaign_id: int) -> Optional[Dict]:
        """Get campaign by ID."""
        try:
            response = self.session.get(f"{self.base_url}/api/v1/campaigns/{campaign_id}")
            return self._handle_response(response)
        except requests.RequestException as e:
            st.error(f"Failed to connect to API: {e}")
            return None
    
    def create_campaign(self, name: str, description: str = None) -> Optional[Dict]:
        """Create a new campaign."""
        data = {"name": name}
        if description:
            data["description"] = description
        
        try:
            response = self.session.post(f"{self.base_url}/api/v1/campaigns/", json=data)
            return self._handle_response(response)
        except requests.RequestException as e:
            st.error(f"Failed to connect to API: {e}")
            return None
    
    # Persona endpoints
    def get_personas(self, campaign_id: Optional[int] = None) -> Optional[List[Dict]]:
        """Get all personas, optionally filtered by campaign."""
        params = {}
        if campaign_id is not None:
            params["campaign_id"] = campaign_id
        
        try:
            response = self.session.get(f"{self.base_url}/api/v1/personas/", params=params)
            return self._handle_response(response)
        except requests.RequestException as e:
            st.error(f"Failed to connect to API: {e}")
            return None
    
    def get_persona(self, persona_id: int) -> Optional[Dict]:
        """Get persona by ID."""
        try:
            response = self.session.get(f"{self.base_url}/api/v1/personas/{persona_id}")
            return self._handle_response(response)
        except requests.RequestException as e:
            st.error(f"Failed to connect to API: {e}")
            return None
    
    def create_persona(self, name: str, backstory: str, personality: str, 
                      campaign_id: int, tag_ids: List[int] = None) -> Optional[Dict]:
        """Create a new persona."""
        data = {
            "name": name,
            "backstory": backstory,
            "personality": personality,
            "campaign_id": campaign_id,
            "tag_ids": tag_ids or []
        }
        
        try:
            response = self.session.post(f"{self.base_url}/api/v1/personas/", json=data)
            return self._handle_response(response)
        except requests.RequestException as e:
            st.error(f"Failed to connect to API: {e}")
            return None
    
    # Tag endpoints
    def get_tags(self) -> Optional[List[Dict]]:
        """Get all tags."""
        try:
            response = self.session.get(f"{self.base_url}/api/v1/tags/")
            return self._handle_response(response)
        except requests.RequestException as e:
            st.error(f"Failed to connect to API: {e}")
            return None
    
    def get_tag(self, tag_id: int) -> Optional[Dict]:
        """Get tag by ID."""
        try:
            response = self.session.get(f"{self.base_url}/api/v1/tags/{tag_id}")
            return self._handle_response(response)
        except requests.RequestException as e:
            st.error(f"Failed to connect to API: {e}")
            return None
    
    # Utility methods
    def health_check(self) -> bool:
        """Check if API server is healthy."""
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=5)
            return response.status_code == 200
        except:
            return False


@st.cache_resource
def get_api_client() -> APIClient:
    """Get cached API client instance."""
    return APIClient()