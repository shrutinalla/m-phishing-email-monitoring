from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from database import get_db
from tracking_models import ClickLog
from campaign_models import Campaign
from models import Employee

router = APIRouter(tags=["Reports"])


@router.get("/reports")
def get_reports(db: Session = Depends(get_db)):

    total_campaigns = db.query(Campaign).count()

    total_employees = db.query(Employee).count()

    total_clicks = db.query(ClickLog).count()

    clicked_employees = (
        db.query(func.count(func.distinct(ClickLog.employee_id)))
        .scalar()
    )

    if clicked_employees is None:
        clicked_employees = 0

    overall_click_rate = 0

    if total_employees > 0:
        overall_click_rate = round(
            (clicked_employees / total_employees) * 100,
            2
        )

    campaigns = db.query(Campaign).all()

    campaign_reports = []

    for campaign in campaigns:

        campaign_clicks = (
            db.query(ClickLog)
            .filter(ClickLog.campaign_id == campaign.id)
            .count()
        )

        campaign_reports.append(
            {
                "campaign_id": campaign.id,
                "campaign_name": campaign.campaign_name,
                "status": campaign.status,
                "emails_clicked": campaign_clicks,
                "start_date": campaign.start_date,
                "end_date": campaign.end_date
            }
        )

    return {

        "summary": {

            "total_campaigns": total_campaigns,

            "total_employees": total_employees,

            "employees_clicked": clicked_employees,

            "total_clicks": total_clicks,

            "overall_click_rate": overall_click_rate

        },

        "campaign_reports": campaign_reports

    }