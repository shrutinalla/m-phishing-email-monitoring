from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from io import StringIO
import csv

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
    ) or 0

    overall_click_rate = (
        round((clicked_employees / total_employees) * 100, 2)
        if total_employees > 0
        else 0
    )

    draft_count = db.query(Campaign).filter(
        Campaign.status == "Draft"
    ).count()

    running_count = db.query(Campaign).filter(
        Campaign.status == "Running"
    ).count()

    completed_count = db.query(Campaign).filter(
        Campaign.status == "Completed"
    ).count()

    scheduled_count = db.query(Campaign).filter(
        Campaign.status == "Scheduled"
    ).count()

    failed_count = db.query(Campaign).filter(
        Campaign.status == "Failed"
    ).count()

    campaigns = db.query(Campaign).order_by(
        Campaign.created_at.desc()
    ).all()

    campaign_reports = []

    for campaign in campaigns:

        click_count = db.query(ClickLog).filter(
            ClickLog.campaign_id == campaign.id
        ).count()

        click_rate = (
            round((click_count / campaign.total_recipients) * 100, 2)
            if campaign.total_recipients > 0
            else 0
        )

        campaign_reports.append(
            {
                "campaign_id": campaign.id,
                "campaign_name": campaign.campaign_name,
                "email_subject": campaign.email_subject,
                "email_template": campaign.email_template,
                "difficulty": campaign.difficulty,
                "status": campaign.status,
                "created_at": campaign.created_at,
                "start_date": campaign.start_date,
                "end_date": campaign.end_date,
                "total_recipients": campaign.total_recipients,
                "emails_sent": campaign.emails_sent,
                "emails_failed": campaign.emails_failed,
                "emails_clicked": click_count,
                "click_rate": click_rate,
            }
        )

    return {
        "summary": {
            "total_campaigns": total_campaigns,
            "draft": draft_count,
            "running": running_count,
            "completed": completed_count,
            "scheduled": scheduled_count,
            "failed": failed_count,
            "total_employees": total_employees,
            "employees_clicked": clicked_employees,
            "total_clicks": total_clicks,
            "overall_click_rate": overall_click_rate,
        },
        "campaign_reports": campaign_reports,
    }


@router.get("/reports/export")
def export_reports(db: Session = Depends(get_db)):

    campaigns = db.query(Campaign).order_by(
        Campaign.created_at.desc()
    ).all()

    output = StringIO()

    writer = csv.writer(output)

    writer.writerow([
        "Campaign Name",
        "Subject",
        "Template",
        "Difficulty",
        "Status",
        "Recipients",
        "Emails Sent",
        "Emails Failed",
        "Emails Clicked",
        "Click Rate (%)",
        "Created At",
        "Start Date",
        "End Date",
    ])

    for campaign in campaigns:

        click_count = db.query(ClickLog).filter(
            ClickLog.campaign_id == campaign.id
        ).count()

        click_rate = (
            round((click_count / campaign.total_recipients) * 100, 2)
            if campaign.total_recipients > 0
            else 0
        )

        writer.writerow([
            campaign.campaign_name,
            campaign.email_subject,
            campaign.email_template,
            campaign.difficulty,
            campaign.status,
            campaign.total_recipients,
            campaign.emails_sent,
            campaign.emails_failed,
            click_count,
            click_rate,
            campaign.created_at,
            campaign.start_date,
            campaign.end_date,
        ])

    output.seek(0)

    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=campaign_reports.csv"
        },
    )