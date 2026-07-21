from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Employee
from campaign_models import Campaign
from email_service import send_phishing_email
from datetime import datetime
from fastapi import HTTPException

router = APIRouter()


@router.post("/send-campaign/{campaign_id}")
def send_campaign(
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

    employees = db.query(Employee).all()

    sent = 0

    for emp in employees:

        send_phishing_email(
            emp.email,
            emp.id,
            campaign_id
        )

        sent += 1

    campaign.status = "Running"
    campaign.start_date = datetime.utcnow()

    db.commit()

    return {

        "message": "Campaign sent successfully",

        "campaign_id": campaign.id,

        "campaign_name": campaign.campaign_name,

        "emails_sent": sent,

        "status": campaign.status

    }