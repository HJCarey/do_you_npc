"""Campaign API routes."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from do_you_npc.api.dependencies import get_db
from do_you_npc.api.schemas import Campaign, CampaignCreate, CampaignUpdate, CampaignWithPersonas
from do_you_npc.db.crud import CampaignCRUD

router = APIRouter()


@router.post("/", response_model=Campaign)
def create_campaign(
    campaign: CampaignCreate,
    db: Session = Depends(get_db)
):
    """Create a new campaign."""
    try:
        db_campaign = CampaignCRUD.create(
            session=db,
            name=campaign.name,
            description=campaign.description
        )
        return db_campaign
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[Campaign])
def list_campaigns(db: Session = Depends(get_db)):
    """Get all campaigns."""
    campaigns = CampaignCRUD.get_all(session=db)
    return campaigns


@router.get("/{campaign_id}", response_model=CampaignWithPersonas)
def get_campaign(campaign_id: int, db: Session = Depends(get_db)):
    """Get a campaign by ID."""
    campaign = CampaignCRUD.get_by_id(session=db, campaign_id=campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign


@router.put("/{campaign_id}", response_model=Campaign)
def update_campaign(
    campaign_id: int,
    campaign_update: CampaignUpdate,
    db: Session = Depends(get_db)
):
    """Update a campaign."""
    update_data = campaign_update.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    updated_campaign = CampaignCRUD.update(
        session=db,
        campaign_id=campaign_id,
        **update_data
    )
    if not updated_campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return updated_campaign


@router.delete("/{campaign_id}")
def delete_campaign(campaign_id: int, db: Session = Depends(get_db)):
    """Delete a campaign."""
    success = CampaignCRUD.delete(session=db, campaign_id=campaign_id)
    if not success:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return {"message": "Campaign deleted successfully"}