from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from database import get_db
from tracking_models import ClickLog
from models import Employee
from campaign_models import Campaign


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


@router.get("/summary")
def analytics_summary(
    db: Session = Depends(get_db)
):

    total_clicks = db.query(
        func.count(ClickLog.id)
    ).scalar()


    return {
        "total_clicks": total_clicks
    }

@router.get("/click-rate")
def click_rate(
    db: Session = Depends(get_db)
):

    total_emails = db.query(
        func.count(Employee.id)
    ).scalar()


    total_clicks = db.query(
        func.count(ClickLog.id)
    ).scalar()


    click_rate = 0

    if total_emails > 0:
        click_rate = (
            total_clicks / total_emails
        ) * 100


    return {

        "total_emails_sent": total_emails,

        "total_clicks": total_clicks,

        "click_rate_percentage": round(click_rate,2)

    }
@router.get("/risky-employees")
def risky_employees(
    db: Session = Depends(get_db)
):

    employees = db.query(Employee).filter(
        Employee.clicked == True
    ).all()


    result = []


    for emp in employees:

        if emp.submitted_credentials:

            risk = "High"

        else:

            risk = "Medium"


        result.append({

            "employee_id": emp.id,

            "name": emp.name,

            "email": emp.email,

            "department": emp.department,

            "risk_level": risk

        })


    return result

@router.get("/campaign-risk")
def campaign_risk(
    db: Session = Depends(get_db)
):

    campaigns = db.query(Campaign).all()

    result = []


    for campaign in campaigns:

        clicks = db.query(
            func.count(ClickLog.id)
        ).filter(
            ClickLog.campaign_id == campaign.id
        ).scalar()


        risk_score = 0

        if campaign.emails_sent > 0:
            risk_score = (
                clicks / campaign.emails_sent
            ) * 100


        result.append(
            {
                "campaign_id": campaign.id,
                "campaign_name": campaign.campaign_name,
                "difficulty": campaign.difficulty,
                "emails_sent": campaign.emails_sent,
                "total_clicks": clicks,
                "risk_score": round(risk_score,2)
            }
        )


    return result

@router.get("/department-risk")
def department_risk(
    db: Session = Depends(get_db)
):

    departments = db.query(
        Employee.department,
        func.count(Employee.id)
    ).group_by(
        Employee.department
    ).all()


    result = []


    for department, total in departments:


        clicked = db.query(
            func.count(Employee.id)
        ).filter(

            Employee.department == department,

            Employee.clicked == True

        ).scalar()



        risk_score = 0


        if total > 0:

            risk_score = (
                clicked / total
            ) * 100



        result.append({

            "department": department,

            "total_employees": total,

            "clicked_employees": clicked,

            "risk_score": round(risk_score,2)

        })


    return sorted(
        result,
        key=lambda x: x["risk_score"],
        reverse=True
    )
@router.get("/risk-trend")
def risk_trend(
    db: Session = Depends(get_db)
):

    trends = (
        db.query(
            func.date(ClickLog.clicked_time)
            .label("date"),

            func.count(ClickLog.id)
            .label("clicks")
        )
        .group_by(
            func.date(ClickLog.clicked_time)
        )
        .order_by(
            func.date(ClickLog.clicked_time)
        )
        .all()
    )


    return [
        {
            "date": str(row.date),
            "clicks": row.clicks
        }

        for row in trends
    ]
@router.get("/campaign-performance")
def campaign_performance(
    db: Session = Depends(get_db)
):

    campaigns = db.query(
        Campaign
    ).all()


    result = []


    for campaign in campaigns:


        clicks = db.query(
            func.count(ClickLog.id)
        ).filter(
            ClickLog.campaign_id == campaign.id
        ).scalar()



        risk = 0


        if campaign.emails_sent > 0:

            risk = (
                clicks /
                campaign.emails_sent
            ) * 100



        result.append({

            "campaign_name":
                campaign.campaign_name,

            "emails_sent":
                campaign.emails_sent,

            "clicks":
                clicks,

            "risk_percentage":
                round(risk,2)

        })


    return result
@router.get("/threat-map")
def threat_map(
    db: Session = Depends(get_db)
):

    locations = (
        db.query(

            ClickLog.ip_address,

            func.count(
                ClickLog.id
            ).label("attempts")

        )
        .group_by(
            ClickLog.ip_address
        )
        .order_by(
            func.count(
                ClickLog.id
            ).desc()
        )
        .all()
    )


    return [

        {
            "ip_address": row.ip_address,
            "attempts": row.attempts
        }

        for row in locations

    ]
@router.get("/dashboard")
def dashboard_summary(
    db: Session = Depends(get_db)
):

    total_employees = db.query(
        func.count(Employee.id)
    ).scalar()


    total_campaigns = db.query(
        func.count(Campaign.id)
    ).scalar()


    total_clicks = db.query(
        func.count(ClickLog.id)
    ).scalar()


    high_risk = db.query(
        func.count(Employee.id)
    ).filter(
        Employee.submitted_credentials == True
    ).scalar()


    return {

        "total_employees":
            total_employees,

        "total_campaigns":
            total_campaigns,

        "total_clicks":
            total_clicks,

        "high_risk_employees":
            high_risk

    }