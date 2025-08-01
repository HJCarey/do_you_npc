"""Pydantic schemas for API request/response models."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class TagBase(BaseModel):
    """Base schema for Tag."""
    name: str
    text_body: str


class TagCreate(TagBase):
    """Schema for creating a Tag."""
    pass


class TagUpdate(BaseModel):
    """Schema for updating a Tag."""
    name: Optional[str] = None
    text_body: Optional[str] = None


class Tag(TagBase):
    """Schema for Tag response."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime
    updated_at: datetime


class PromptBase(BaseModel):
    """Base schema for Prompt."""
    name: str
    text_body: str


class PromptCreate(PromptBase):
    """Schema for creating a Prompt."""
    pass


class PromptUpdate(BaseModel):
    """Schema for updating a Prompt."""
    name: Optional[str] = None
    text_body: Optional[str] = None


class Prompt(PromptBase):
    """Schema for Prompt response."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime
    updated_at: datetime


class CampaignBase(BaseModel):
    """Base schema for Campaign."""
    name: str
    description: Optional[str] = None


class CampaignCreate(CampaignBase):
    """Schema for creating a Campaign."""
    pass


class CampaignUpdate(BaseModel):
    """Schema for updating a Campaign."""
    name: Optional[str] = None
    description: Optional[str] = None


class Campaign(CampaignBase):
    """Schema for Campaign response."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime
    updated_at: datetime


class CampaignWithPersonas(Campaign):
    """Schema for Campaign response with personas."""
    personas: List["Persona"] = []


class PersonaBase(BaseModel):
    """Base schema for Persona."""
    name: str
    backstory: str
    personality: str
    campaign_id: int


class PersonaCreate(PersonaBase):
    """Schema for creating a Persona."""
    tag_ids: Optional[List[int]] = []


class PersonaUpdate(BaseModel):
    """Schema for updating a Persona."""
    name: Optional[str] = None
    backstory: Optional[str] = None
    personality: Optional[str] = None
    campaign_id: Optional[int] = None
    tag_ids: Optional[List[int]] = None


class Persona(PersonaBase):
    """Schema for Persona response."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime
    updated_at: datetime
    campaign: Campaign
    tags: List[Tag] = []


# Forward reference resolution
CampaignWithPersonas.model_rebuild()