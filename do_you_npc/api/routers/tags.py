"""Tag API routes."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from do_you_npc.api.dependencies import get_db
from do_you_npc.api.schemas import Tag, TagCreate, TagUpdate
from do_you_npc.db.crud import TagCRUD

router = APIRouter()


@router.post("/", response_model=Tag)
def create_tag(
    tag: TagCreate,
    db: Session = Depends(get_db)
):
    """Create a new tag."""
    try:
        db_tag = TagCRUD.create(
            session=db,
            name=tag.name,
            text_body=tag.text_body
        )
        return db_tag
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[Tag])
def list_tags(db: Session = Depends(get_db)):
    """Get all tags."""
    tags = TagCRUD.get_all(session=db)
    return tags


@router.get("/{tag_id}", response_model=Tag)
def get_tag(tag_id: int, db: Session = Depends(get_db)):
    """Get a tag by ID."""
    tag = TagCRUD.get_by_id(session=db, tag_id=tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag


@router.get("/name/{tag_name}", response_model=Tag)
def get_tag_by_name(tag_name: str, db: Session = Depends(get_db)):
    """Get a tag by name."""
    tag = TagCRUD.get_by_name(session=db, name=tag_name)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag


@router.put("/{tag_id}", response_model=Tag)
def update_tag(
    tag_id: int,
    tag_update: TagUpdate,
    db: Session = Depends(get_db)
):
    """Update a tag."""
    update_data = tag_update.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    updated_tag = TagCRUD.update(
        session=db,
        tag_id=tag_id,
        **update_data
    )
    if not updated_tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return updated_tag


@router.delete("/{tag_id}")
def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    """Delete a tag."""
    success = TagCRUD.delete(session=db, tag_id=tag_id)
    if not success:
        raise HTTPException(status_code=404, detail="Tag not found")
    return {"message": "Tag deleted successfully"}