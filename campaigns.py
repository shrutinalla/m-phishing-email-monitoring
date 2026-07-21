from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_

from database import get_db
from campaign_models import Campaign
from campaign_schemas import CampaignCreate, CampaignUpdate

router = APIRouter()


@router.post("/campaigns")
def create_campaign(campaign: CampaignCreate, db: Session = Depends(get_db)):

    new_campaign = Campaign(
        campaign_name=campaign.campaign_name,
        email_subject=campaign.email_subject,
        email_template=campaign.email_template,
        difficulty=campaign.difficulty,
        status=campaign.status
    )

    db.add(new_campaign)
    db.commit()
    db.refresh(new_campaign)

    return {
        "message": "Campaign created successfully",
        "campaign_id": new_campaign.id
    }


@router.get("/campaigns")
def get_campaigns(db: Session = Depends(get_db)):
    return db.query(Campaign).all()

@router.get("/campaigns/search")
def search_campaign(keyword: str, db: Session = Depends(get_db)):

    campaigns = db.query(Campaign).filter(
        or_(
            Campaign.campaign_name.ilike(f"%{keyword}%"),
            Campaign.email_subject.ilike(f"%{keyword}%"),
            Campaign.difficulty.ilike(f"%{keyword}%"),
            Campaign.status.ilike(f"%{keyword}%")
        )
    ).all()

    return campaigns
@router.get("/campaigns/dashboard")
def campaign_dashboard(
    db: Session = Depends(get_db)
):

    total = db.query(Campaign).count()

    draft = db.query(Campaign).filter(
        Campaign.status == "Draft"
    ).count()

    active = db.query(Campaign).filter(
        Campaign.status == "Active"
    ).count()

    completed = db.query(Campaign).filter(
        Campaign.status == "Completed"
    ).count()

    return {
        "total_campaigns": total,
        "draft_campaigns": draft,
        "active_campaigns": active,
        "completed_campaigns": completed
    }


@router.get("/campaigns/{campaign_id}")
def get_campaign(campaign_id: int, db: Session = Depends(get_db)):

    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id
    ).first()

    if campaign is None:
        raise HTTPException(status_code=404, detail="Campaign not found")

    return campaign


@router.put("/campaigns/{campaign_id}")
def update_campaign(
    campaign_id: int,
    updated: CampaignUpdate,
    db: Session = Depends(get_db)
):

    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id
    ).first()

    if campaign is None:
        raise HTTPException(status_code=404, detail="Campaign not found")

    campaign.campaign_name = updated.campaign_name
    campaign.email_subject = updated.email_subject
    campaign.email_template = updated.email_template
    campaign.difficulty = updated.difficulty
    campaign.status = updated.status

    db.commit()

    return {"message": "Campaign updated successfully"}


@router.delete("/campaigns/{campaign_id}")
def delete_campaign(campaign_id: int, db: Session = Depends(get_db)):

    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id
    ).first()

    if campaign is None:
        raise HTTPException(status_code=404, detail="Campaign not found")

    db.delete(campaign)
    db.commit()

    return {"message": "Campaign deleted successfully"}


