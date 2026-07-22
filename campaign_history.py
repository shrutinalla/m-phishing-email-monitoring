from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from campaign_models import Campaign
from tracking_models import ClickLog

router = APIRouter()


@router.get("/campaigns/{campaign_id}/history")
def campaign_history(
    campaign_id: int,
    db: Session = Depends(get_db)
):

    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id
    ).first()

    if campaign is None:
        raise HTTPException(
            status_code=404,
            detail="Campaign not found"
        )

    clicks = db.query(ClickLog).filter(
        ClickLog.campaign_id == campaign_id
    ).all()

    history = []

    for click in clicks:

        history.append({
            "employee_id": click.employee_id,
            "email": click.email,
            "clicked_time": click.clicked_time,
            "ip_address": click.ip_address,
            "user_agent": click.user_agent
        })

    return {
        "campaign_id": campaign.id,
        "campaign_name": campaign.campaign_name,
        "status": campaign.status,
        "difficulty": campaign.difficulty,
        "total_clicks": len(history),
        "history": history
    }