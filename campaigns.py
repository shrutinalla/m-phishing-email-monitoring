from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_

from database import get_db
from campaign_models import Campaign
from send_mail import send_phishing_email
from models import Employee
from tracking_models import ClickLog
from template_models import EmailTemplate

from campaign_schemas import (
    CampaignCreate,
    CampaignUpdate,
    CampaignStatusUpdate,
    CampaignSchedule
)

router = APIRouter()


'''@router.post("/campaigns")
def create_campaign(campaign: CampaignCreate, db: Session = Depends(get_db)):

    new_campaign = Campaign(
        campaign_name=campaign.campaign_name,
        email_subject=campaign.email_subject,
        email_template=campaign.email_template,
        difficulty=campaign.difficulty,
        status=campaign.status,
        template_id=campaign.template_id
    )

    db.add(new_campaign)
    db.commit()
    db.refresh(new_campaign)

    return {
        "message": "Campaign created successfully",
        "campaign_id": new_campaign.id
    }'''

@router.post("/campaigns")
def create_campaign(campaign: CampaignCreate, db: Session = Depends(get_db)):
    try:
        print("Received:", campaign)
        existing_campaign = db.query(Campaign).filter(
            Campaign.campaign_name == campaign.campaign_name
            ).first()
        if existing_campaign:
            raise HTTPException(
                status_code=400,
                detail="Campaign name already exists"
                )

        new_campaign = Campaign(
            campaign_name=campaign.campaign_name,
            email_subject=campaign.email_subject,
            email_template=campaign.email_template,
            difficulty=campaign.difficulty,
            status=campaign.status,
            template_id=campaign.template_id
        )

        db.add(new_campaign)
        db.commit()
        db.refresh(new_campaign)

        return {
            "message": "Campaign created successfully",
            "campaign_id": new_campaign.id
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print("ERROR:", repr(e))
        raise HTTPException(
         status_code=500,
         detail="Internal Server Error"
        )



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

@router.put("/campaigns/{campaign_id}/status")
def update_campaign_status(
    campaign_id: int,
    status: str,
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

    campaign.status = status

    db.commit()

    return {
        "message": "Campaign status updated successfully",
        "status": campaign.status
    }


@router.put("/campaigns/{campaign_id}/schedule")
def schedule_campaign(
    campaign_id: int,
    schedule: CampaignSchedule,
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

    campaign.start_date = schedule.start_date
    campaign.end_date = schedule.end_date
    campaign.status = "Scheduled"

    db.commit()

    return {
        "message": "Campaign scheduled successfully",
        "start_date": campaign.start_date,
        "end_date": campaign.end_date,
         "status": campaign.status
    }

@router.get("/campaigns/{campaign_id}/analytics")
def campaign_analytics(
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

    total_employees = db.query(Employee).count()

    clicked = db.query(Employee).filter(
        Employee.clicked == True
    ).count()

    submitted = db.query(Employee).filter(
        Employee.submitted_credentials == True
    ).count()

    emails_sent = total_employees

    click_rate = 0
    submission_rate = 0

    if total_employees > 0:
        click_rate = round(
            (clicked / total_employees) * 100,
            2
        )

        submission_rate = round(
            (submitted / total_employees) * 100,
            2
        )

    return {

        "campaign_id": campaign.id,

        "campaign_name": campaign.campaign_name,

        "emails_sent": emails_sent,

        "clicked": clicked,

        "submitted_credentials": submitted,

        "click_rate": f"{click_rate}%",

        "submission_rate": f"{submission_rate}%"

    }

@router.get("/campaigns/departments/analytics")
def department_analytics(db: Session = Depends(get_db)):

    departments = db.query(Employee.department).distinct().all()

    result = []

    for dept in departments:

        department = dept[0]

        total = db.query(Employee).filter(
            Employee.department == department
        ).count()

        clicked = db.query(Employee).filter(
            Employee.department == department,
            Employee.clicked == True
        ).count()

        submitted = db.query(Employee).filter(
            Employee.department == department,
            Employee.submitted_credentials == True
        ).count()

        result.append({
            "department": department,
            "employees": total,
            "clicked": clicked,
            "submitted_credentials": submitted
        })

    return result

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

 

@router.get("/campaigns/status/{status}")
def campaigns_by_status(
    status: str,
    db: Session = Depends(get_db)
):

    return db.query(Campaign).filter(
        Campaign.status == status
    ).all()

@router.get("/campaigns/difficulty/{difficulty}")
def campaigns_by_difficulty(
    difficulty: str,
    db: Session = Depends(get_db)
):

    return db.query(Campaign).filter(
        Campaign.difficulty == difficulty
    ).all()

@router.get("/campaigns/statistics")
def campaign_statistics(
    db: Session = Depends(get_db)
):

    total = db.query(Campaign).count()

    easy = db.query(Campaign).filter(
        Campaign.difficulty == "Easy"
    ).count()

    medium = db.query(Campaign).filter(
        Campaign.difficulty == "Medium"
    ).count()

    hard = db.query(Campaign).filter(
        Campaign.difficulty == "Hard"
    ).count()

    return {
        "total_campaigns": total,
        "easy": easy,
        "medium": medium,
        "hard": hard
    }


@router.get("/campaigns/{campaign_id}/analytics")
def campaign_analytics(
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

    total_employees = db.query(Employee).count()

    clicked = db.query(Employee).filter(
        Employee.clicked == True
    ).count()

    submitted = db.query(Employee).filter(
        Employee.submitted_credentials == True
    ).count()

    click_rate = 0
    submission_rate = 0

    if total_employees > 0:
        click_rate = round((clicked / total_employees) * 100, 2)
        submission_rate = round((submitted / total_employees) * 100, 2)

    return {
        "campaign": campaign.campaign_name,
        "total_employees": total_employees,
        "clicked": clicked,
        "submitted_credentials": submitted,
        "click_rate": f"{click_rate}%",
        "submission_rate": f"{submission_rate}%"
    }

@router.put("/campaigns/{campaign_id}/use-template/{template_id}")
def use_template(
    campaign_id: int,
    template_id: int,
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

    template = db.query(EmailTemplate).filter(
        EmailTemplate.id == template_id
    ).first()

    if template is None:
        raise HTTPException(
            status_code=404,
            detail="Template not found"
        )

    campaign.template_id = template.id
    campaign.email_subject = template.subject
    campaign.email_template = template.content

    db.commit()

    return {
        "message": "Template linked successfully",
        "campaign_id": campaign.id,
        "template": template.template_name
    }

@router.post("/campaigns/{campaign_id}/send")
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

    for employee in employees:

        send_phishing_email(
            employee.email,
            campaign.email_subject,
            campaign.email_template,
            employee.id,
            campaign.id
        )

        sent += 1

    campaign.status = "Running"
    db.commit()

    return {
        "message": "Campaign emails sent successfully",
        "emails_sent": sent
    }

@router.get("/campaigns/{campaign_id}/analytics")
def campaign_analytics(
    campaign_id: int,
    db: Session = Depends(get_db)
):

    sent = db.query(Employee).count()

    opened = db.query(ClickLog).filter(
        ClickLog.campaign_id == campaign_id
    ).count()

    clicked = db.query(Employee).filter(
        Employee.clicked == True
    ).count()

    submitted = db.query(Employee).filter(
        Employee.submitted_credentials == True
    ).count()

    if sent == 0:
        success_rate = 0
    else:
        success_rate = round(
            (clicked / sent) * 100,
            2
        )

    return {

        "campaign_id": campaign_id,

        "emails_sent": sent,

        "emails_opened": opened,

        "link_clicks": clicked,

        "credentials_submitted": submitted,

        "click_rate": success_rate

    }