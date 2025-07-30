"""CRUD operations for database models."""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select

from .models import Campaign, Persona, Prompt, Tag


class PersonaCRUD:
    """CRUD operations for Persona model."""
    
    @staticmethod
    def create(session: Session, name: str, backstory: str, personality: str, campaign_id: int, tags: List[Tag] = None) -> Persona:
        """Create a new persona.
        
        Args:
            session: Database session
            name: Persona name
            backstory: Persona backstory
            personality: Persona personality
            campaign_id: Campaign ID this persona belongs to
            tags: List of tags to associate with the persona
            
        Returns:
            Persona: Created persona instance
        """
        persona = Persona(name=name, backstory=backstory, personality=personality, campaign_id=campaign_id)
        if tags:
            persona.tags.extend(tags)
        
        session.add(persona)
        session.commit()
        session.refresh(persona)
        return persona
    
    @staticmethod
    def get_by_id(session: Session, persona_id: int) -> Optional[Persona]:
        """Get a persona by ID.
        
        Args:
            session: Database session
            persona_id: Persona ID
            
        Returns:
            Persona: Persona instance or None if not found
        """
        return session.get(Persona, persona_id)
    
    @staticmethod
    def get_by_name(session: Session, name: str) -> Optional[Persona]:
        """Get a persona by name.
        
        Args:
            session: Database session
            name: Persona name
            
        Returns:
            Persona: Persona instance or None if not found
        """
        stmt = select(Persona).where(Persona.name == name)
        return session.execute(stmt).scalar_one_or_none()
    
    @staticmethod
    def get_all(session: Session, campaign_id: int = None) -> List[Persona]:
        """Get all personas, optionally filtered by campaign.
        
        Args:
            session: Database session
            campaign_id: Optional campaign ID to filter by
            
        Returns:
            List[Persona]: List of personas
        """
        stmt = select(Persona)
        if campaign_id is not None:
            stmt = stmt.where(Persona.campaign_id == campaign_id)
        return list(session.execute(stmt).scalars().all())
    
    @staticmethod
    def get_by_campaign(session: Session, campaign_id: int) -> List[Persona]:
        """Get all personas for a specific campaign.
        
        Args:
            session: Database session
            campaign_id: Campaign ID
            
        Returns:
            List[Persona]: List of personas in the campaign
        """
        stmt = select(Persona).where(Persona.campaign_id == campaign_id)
        return list(session.execute(stmt).scalars().all())
    
    @staticmethod
    def update(session: Session, persona_id: int, **kwargs) -> Optional[Persona]:
        """Update a persona.
        
        Args:
            session: Database session
            persona_id: Persona ID
            **kwargs: Fields to update
            
        Returns:
            Persona: Updated persona instance or None if not found
        """
        persona = session.get(Persona, persona_id)
        if not persona:
            return None
        
        for key, value in kwargs.items():
            if hasattr(persona, key):
                setattr(persona, key, value)
        
        session.commit()
        session.refresh(persona)
        return persona
    
    @staticmethod
    def delete(session: Session, persona_id: int) -> bool:
        """Delete a persona.
        
        Args:
            session: Database session
            persona_id: Persona ID
            
        Returns:
            bool: True if deleted, False if not found
        """
        persona = session.get(Persona, persona_id)
        if not persona:
            return False
        
        session.delete(persona)
        session.commit()
        return True


class PromptCRUD:
    """CRUD operations for Prompt model."""
    
    @staticmethod
    def create(session: Session, name: str, text_body: str) -> Prompt:
        """Create a new prompt.
        
        Args:
            session: Database session
            name: Prompt name
            text_body: Prompt text body
            
        Returns:
            Prompt: Created prompt instance
        """
        prompt = Prompt(name=name, text_body=text_body)
        session.add(prompt)
        session.commit()
        session.refresh(prompt)
        return prompt
    
    @staticmethod
    def get_by_id(session: Session, prompt_id: int) -> Optional[Prompt]:
        """Get a prompt by ID.
        
        Args:
            session: Database session
            prompt_id: Prompt ID
            
        Returns:
            Prompt: Prompt instance or None if not found
        """
        return session.get(Prompt, prompt_id)
    
    @staticmethod
    def get_by_name(session: Session, name: str) -> Optional[Prompt]:
        """Get a prompt by name.
        
        Args:
            session: Database session
            name: Prompt name
            
        Returns:
            Prompt: Prompt instance or None if not found
        """
        stmt = select(Prompt).where(Prompt.name == name)
        return session.execute(stmt).scalar_one_or_none()
    
    @staticmethod
    def get_all(session: Session) -> List[Prompt]:
        """Get all prompts.
        
        Args:
            session: Database session
            
        Returns:
            List[Prompt]: List of all prompts
        """
        stmt = select(Prompt)
        return list(session.execute(stmt).scalars().all())
    
    @staticmethod
    def update(session: Session, prompt_id: int, **kwargs) -> Optional[Prompt]:
        """Update a prompt.
        
        Args:
            session: Database session
            prompt_id: Prompt ID
            **kwargs: Fields to update
            
        Returns:
            Prompt: Updated prompt instance or None if not found
        """
        prompt = session.get(Prompt, prompt_id)
        if not prompt:
            return None
        
        for key, value in kwargs.items():
            if hasattr(prompt, key):
                setattr(prompt, key, value)
        
        session.commit()
        session.refresh(prompt)
        return prompt
    
    @staticmethod
    def delete(session: Session, prompt_id: int) -> bool:
        """Delete a prompt.
        
        Args:
            session: Database session
            prompt_id: Prompt ID
            
        Returns:
            bool: True if deleted, False if not found
        """
        prompt = session.get(Prompt, prompt_id)
        if not prompt:
            return False
        
        session.delete(prompt)
        session.commit()
        return True


class TagCRUD:
    """CRUD operations for Tag model."""
    
    @staticmethod
    def create(session: Session, name: str, text_body: str) -> Tag:
        """Create a new tag.
        
        Args:
            session: Database session
            name: Tag name
            text_body: Tag text body
            
        Returns:
            Tag: Created tag instance
        """
        tag = Tag(name=name, text_body=text_body)
        session.add(tag)
        session.commit()
        session.refresh(tag)
        return tag
    
    @staticmethod
    def get_by_id(session: Session, tag_id: int) -> Optional[Tag]:
        """Get a tag by ID.
        
        Args:
            session: Database session
            tag_id: Tag ID
            
        Returns:
            Tag: Tag instance or None if not found
        """
        return session.get(Tag, tag_id)
    
    @staticmethod
    def get_by_name(session: Session, name: str) -> Optional[Tag]:
        """Get a tag by name.
        
        Args:
            session: Database session
            name: Tag name
            
        Returns:
            Tag: Tag instance or None if not found
        """
        stmt = select(Tag).where(Tag.name == name)
        return session.execute(stmt).scalar_one_or_none()
    
    @staticmethod
    def get_all(session: Session) -> List[Tag]:
        """Get all tags.
        
        Args:
            session: Database session
            
        Returns:
            List[Tag]: List of all tags
        """
        stmt = select(Tag)
        return list(session.execute(stmt).scalars().all())
    
    @staticmethod
    def update(session: Session, tag_id: int, **kwargs) -> Optional[Tag]:
        """Update a tag.
        
        Args:
            session: Database session
            tag_id: Tag ID
            **kwargs: Fields to update
            
        Returns:
            Tag: Updated tag instance or None if not found
        """
        tag = session.get(Tag, tag_id)
        if not tag:
            return None
        
        for key, value in kwargs.items():
            if hasattr(tag, key):
                setattr(tag, key, value)
        
        session.commit()
        session.refresh(tag)
        return tag
    
    @staticmethod
    def delete(session: Session, tag_id: int) -> bool:
        """Delete a tag.
        
        Args:
            session: Database session
            tag_id: Tag ID
            
        Returns:
            bool: True if deleted, False if not found
        """
        tag = session.get(Tag, tag_id)
        if not tag:
            return False
        
        session.delete(tag)
        session.commit()
        return True


class CampaignCRUD:
    """CRUD operations for Campaign model."""
    
    @staticmethod
    def create(session: Session, name: str, description: str = None) -> Campaign:
        """Create a new campaign.
        
        Args:
            session: Database session
            name: Campaign name
            description: Campaign description (optional)
            
        Returns:
            Campaign: Created campaign instance
        """
        campaign = Campaign(name=name, description=description)
        session.add(campaign)
        session.commit()
        session.refresh(campaign)
        return campaign
    
    @staticmethod
    def get_by_id(session: Session, campaign_id: int) -> Optional[Campaign]:
        """Get a campaign by ID.
        
        Args:
            session: Database session
            campaign_id: Campaign ID
            
        Returns:
            Campaign: Campaign instance or None if not found
        """
        return session.get(Campaign, campaign_id)
    
    @staticmethod
    def get_by_name(session: Session, name: str) -> Optional[Campaign]:
        """Get a campaign by name.
        
        Args:
            session: Database session
            name: Campaign name
            
        Returns:
            Campaign: Campaign instance or None if not found
        """
        stmt = select(Campaign).where(Campaign.name == name)
        return session.execute(stmt).scalar_one_or_none()
    
    @staticmethod
    def get_all(session: Session) -> List[Campaign]:
        """Get all campaigns.
        
        Args:
            session: Database session
            
        Returns:
            List[Campaign]: List of all campaigns
        """
        stmt = select(Campaign)
        return list(session.execute(stmt).scalars().all())
    
    @staticmethod
    def update(session: Session, campaign_id: int, **kwargs) -> Optional[Campaign]:
        """Update a campaign.
        
        Args:
            session: Database session
            campaign_id: Campaign ID
            **kwargs: Fields to update
            
        Returns:
            Campaign: Updated campaign instance or None if not found
        """
        campaign = session.get(Campaign, campaign_id)
        if not campaign:
            return None
        
        for key, value in kwargs.items():
            if hasattr(campaign, key):
                setattr(campaign, key, value)
        
        session.commit()
        session.refresh(campaign)
        return campaign
    
    @staticmethod
    def delete(session: Session, campaign_id: int) -> bool:
        """Delete a campaign.
        
        Args:
            session: Database session
            campaign_id: Campaign ID
            
        Returns:
            bool: True if deleted, False if not found
        """
        campaign = session.get(Campaign, campaign_id)
        if not campaign:
            return False
        
        session.delete(campaign)
        session.commit()
        return True