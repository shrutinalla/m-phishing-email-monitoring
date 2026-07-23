from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Employee
from campaign_models import Campaign
from tracking_models import ClickLog

router = APIRouter(tags=["Live Tracking"])


@router.get("/tracking/live")
def live_tracking(db: Session = Depends(get_db)):

    emails_sent = db.query(Employee).count()

    emails_opened = db.query(ClickLog).count()

    link_clicks = db.query(Employee).filter(
        Employee.clicked == True
    ).count()

    credentials = db.query(Employee).filter(
        Employee.submitted_credentials == True
    ).count()

    active_campaigns = db.query(Campaign).filter(
        Campaign.status == "Running"
    ).count()

    return {
        "emails_sent": emails_sent,
        "emails_opened": emails_opened,
        "link_clicks": link_clicks,
        "credentials_submitted": credentials,
        "active_campaigns": active_campaigns
    }


@router.get("/tracking/recent")
def recent_clicks(db: Session = Depends(get_db)):

    logs = db.query(ClickLog).order_by(
        ClickLog.clicked_time.desc()
    ).limit(10).all()

    return logs


@router.get("/tracking/active-campaigns")
def active_campaigns(db: Session = Depends(get_db)):

    campaigns = db.query(Campaign).filter(
        Campaign.status == "Running"
    ).all()

    return campaigns


@router.get("/tracking/employees")
def employee_tracking(db: Session = Depends(get_db)):

    employees = db.query(Employee).all()

    return [
        {
            "id": emp.id,
            "name": emp.name,
            "email": emp.email,
            "clicked": emp.clicked,
            "submitted_credentials": emp.submitted_credentials
        }
        for emp in employees
    ]


@router.get("/tracking/campaign/{campaign_id}")
def campaign_live_status(
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

    total = db.query(Employee).count()

    opened = db.query(ClickLog).filter(
        ClickLog.campaign_id == campaign_id
    ).count()

    clicked = db.query(Employee).filter(
        Employee.clicked == True
    ).count()

    submitted = db.query(Employee).filter(
        Employee.submitted_credentials == True
    ).count()

    return {
        "campaign_id": campaign.id,
        "campaign_name": campaign.campaign_name,
        "status": campaign.status,
        "emails_sent": total,
        "emails_opened": opened,
        "clicked": clicked,
        "submitted": submitted
    }