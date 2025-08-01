"""Prompt API routes."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from do_you_npc.api.dependencies import get_db
from do_you_npc.api.schemas import Prompt, PromptCreate, PromptUpdate
from do_you_npc.db.crud import PromptCRUD

router = APIRouter()


@router.post("/", response_model=Prompt)
def create_prompt(
    prompt: PromptCreate,
    db: Session = Depends(get_db)
):
    """Create a new prompt."""
    try:
        db_prompt = PromptCRUD.create(
            session=db,
            name=prompt.name,
            text_body=prompt.text_body
        )
        return db_prompt
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[Prompt])
def list_prompts(db: Session = Depends(get_db)):
    """Get all prompts."""
    prompts = PromptCRUD.get_all(session=db)
    return prompts


@router.get("/{prompt_id}", response_model=Prompt)
def get_prompt(prompt_id: int, db: Session = Depends(get_db)):
    """Get a prompt by ID."""
    prompt = PromptCRUD.get_by_id(session=db, prompt_id=prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return prompt


@router.get("/name/{prompt_name}", response_model=Prompt)
def get_prompt_by_name(prompt_name: str, db: Session = Depends(get_db)):
    """Get a prompt by name."""
    prompt = PromptCRUD.get_by_name(session=db, name=prompt_name)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return prompt


@router.put("/{prompt_id}", response_model=Prompt)
def update_prompt(
    prompt_id: int,
    prompt_update: PromptUpdate,
    db: Session = Depends(get_db)
):
    """Update a prompt."""
    update_data = prompt_update.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    updated_prompt = PromptCRUD.update(
        session=db,
        prompt_id=prompt_id,
        **update_data
    )
    if not updated_prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return updated_prompt


@router.delete("/{prompt_id}")
def delete_prompt(prompt_id: int, db: Session = Depends(get_db)):
    """Delete a prompt."""
    success = PromptCRUD.delete(session=db, prompt_id=prompt_id)
    if not success:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return {"message": "Prompt deleted successfully"}