"""Persona API routes."""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from do_you_npc.api.dependencies import get_db
from do_you_npc.api.schemas import Persona, PersonaCreate, PersonaUpdate
from do_you_npc.db.crud import PersonaCRUD, TagCRUD

router = APIRouter()


@router.post("/", response_model=Persona)
def create_persona(
    persona: PersonaCreate,
    db: Session = Depends(get_db)
):
    """Create a new persona."""
    try:
        tags = []
        if persona.tag_ids:
            for tag_id in persona.tag_ids:
                tag = TagCRUD.get_by_id(session=db, tag_id=tag_id)
                if not tag:
                    raise HTTPException(status_code=400, detail=f"Tag with ID {tag_id} not found")
                tags.append(tag)
        
        db_persona = PersonaCRUD.create(
            session=db,
            name=persona.name,
            backstory=persona.backstory,
            personality=persona.personality,
            campaign_id=persona.campaign_id,
            tags=tags
        )
        return db_persona
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[Persona])
def list_personas(
    campaign_id: Optional[int] = Query(None, description="Filter personas by campaign ID"),
    db: Session = Depends(get_db)
):
    """Get all personas, optionally filtered by campaign."""
    personas = PersonaCRUD.get_all(session=db, campaign_id=campaign_id)
    return personas


@router.get("/{persona_id}", response_model=Persona)
def get_persona(persona_id: int, db: Session = Depends(get_db)):
    """Get a persona by ID."""
    persona = PersonaCRUD.get_by_id(session=db, persona_id=persona_id)
    if not persona:
        raise HTTPException(status_code=404, detail="Persona not found")
    return persona


@router.put("/{persona_id}", response_model=Persona)
def update_persona(
    persona_id: int,
    persona_update: PersonaUpdate,
    db: Session = Depends(get_db)
):
    """Update a persona."""
    update_data = persona_update.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    tag_ids = update_data.pop('tag_ids', None)
    
    if tag_ids is not None:
        persona = PersonaCRUD.get_by_id(session=db, persona_id=persona_id)
        if not persona:
            raise HTTPException(status_code=404, detail="Persona not found")
        
        persona.tags.clear()
        
        for tag_id in tag_ids:
            tag = TagCRUD.get_by_id(session=db, tag_id=tag_id)
            if not tag:
                raise HTTPException(status_code=400, detail=f"Tag with ID {tag_id} not found")
            persona.tags.append(tag)
        
        db.commit()
        db.refresh(persona)
    
    if update_data:
        updated_persona = PersonaCRUD.update(
            session=db,
            persona_id=persona_id,
            **update_data
        )
        if not updated_persona:
            raise HTTPException(status_code=404, detail="Persona not found")
        return updated_persona
    
    return PersonaCRUD.get_by_id(session=db, persona_id=persona_id)


@router.delete("/{persona_id}")
def delete_persona(persona_id: int, db: Session = Depends(get_db)):
    """Delete a persona."""
    success = PersonaCRUD.delete(session=db, persona_id=persona_id)
    if not success:
        raise HTTPException(status_code=404, detail="Persona not found")
    return {"message": "Persona deleted successfully"}