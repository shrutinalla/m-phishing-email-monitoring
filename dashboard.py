from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Employee
from campaign_models import Campaign
print(Campaign.__table__.columns.keys())
from tracking_models import ClickLog

router = APIRouter()


@router.get("/dashboard")
def dashboard_summary(
    db: Session = Depends(get_db)
):

    # Total Employees
    total_employees = db.query(Employee).count()

    # Total Campaigns
    total_campaigns = db.query(Campaign).count()

    # Running Campaigns
    running_campaigns = (
        db.query(Campaign)
        .filter(Campaign.status == "Running")
        .count()
    )

    # Completed Campaigns
    completed_campaigns = (
        db.query(Campaign)
        .filter(Campaign.status == "Completed")
        .count()
    )

    # Total Clicks
    total_clicks = db.query(ClickLog).count()

    # High Risk Employees
    high_risk_employees = (
        db.query(Employee)
        .filter(Employee.clicked == True)
        .count()
    )

    # Email Statistics
    campaigns = db.query(Campaign).all()

    emails_sent = sum(
        campaign.emails_sent or 0
        for campaign in campaigns
    )

    emails_failed = sum(
        campaign.emails_failed or 0
        for campaign in campaigns
    )

    # Click Rate
    if emails_sent > 0:
        click_rate = round(
            (total_clicks / emails_sent) * 100,
            2
        )
    else:
        click_rate = 0

    return {

        "total_employees": total_employees,

        "total_campaigns": total_campaigns,

        "running_campaigns": running_campaigns,

        "completed_campaigns": completed_campaigns,

        "emails_sent": emails_sent,

        "emails_failed": emails_failed,

        "total_clicks": total_clicks,

        "click_rate": click_rate,

        "high_risk_employees": high_risk_employees

    }