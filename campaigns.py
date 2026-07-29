import os
import shutil
import uuid




from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_

from database import get_db
from campaign_models import Campaign
from models import Employee
from tracking_models import ClickLog
from template_models import EmailTemplate
from auth_dependency import get_current_admin
from audit_models import AuditLog
from zoneinfo import ZoneInfo
from datetime import datetime
from fastapi import UploadFile, File
from campaign_schemas import (
    CampaignCreate,
    CampaignUpdate,
    CampaignSchedule
)

router = APIRouter()

# -------------------------------
# CREATE CAMPAIGN
# -------------------------------

@router.post("/campaigns")
def create_campaign(
    campaign: CampaignCreate,
    db: Session = Depends(get_db)
):

    campaign_name = campaign.campaign_name

    counter = 1

    while db.query(Campaign).filter(
        Campaign.campaign_name == campaign_name
    ).first():

        campaign_name = f"{campaign.campaign_name} ({counter})"
        counter += 1

    new_campaign = Campaign(

        campaign_name=campaign_name,

        email_subject=campaign.email_subject,

        email_template=campaign.email_template,

        difficulty=campaign.difficulty,

        status=campaign.status,

        template_id=campaign.template_id

    )

    db.add(new_campaign)
    db.commit()
    db.refresh(new_campaign)

    log = AuditLog(
        action="Campaign Created",
        performed_by="Admin",
        module="Campaign",
        details=f"Campaign '{new_campaign.campaign_name}' created",
        timestamp=datetime.now(ZoneInfo("Asia/Kolkata"))
    )

    db.add(log)
    db.commit()

    return {
        "message": "Campaign created successfully",
        "campaign_id": new_campaign.id,
        "campaign_name": new_campaign.campaign_name
    }


# -------------------------------
# GET ALL CAMPAIGNS
# -------------------------------

@router.get("/campaigns")
def get_campaigns(
    db: Session = Depends(get_db),
    admin: str = Depends(get_current_admin)
):

    return db.query(Campaign).all()


# -------------------------------
# SEARCH CAMPAIGN
# -------------------------------

@router.get("/campaigns/search")
def search_campaign(
    keyword: str,
    db: Session = Depends(get_db),
    admin: str = Depends(get_current_admin)
):

    campaigns = db.query(Campaign).filter(

        or_(

            Campaign.campaign_name.ilike(
                f"%{keyword}%"
            ),

            Campaign.email_subject.ilike(
                f"%{keyword}%"
            ),

            Campaign.difficulty.ilike(
                f"%{keyword}%"
            ),

            Campaign.status.ilike(
                f"%{keyword}%"
            )

        )

    ).all()

    return campaigns


# -------------------------------
# CAMPAIGN DASHBOARD
# -------------------------------

@router.get("/campaigns/dashboard")
def campaign_dashboard(
    db: Session = Depends(get_db),
    admin: str = Depends(get_current_admin)
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


# -------------------------------
# GET SINGLE CAMPAIGN
# -------------------------------

@router.get("/campaigns/{campaign_id}")
def get_campaign(
    campaign_id: int,
    db: Session = Depends(get_db),
):

    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id
    ).first()

    if campaign is None:

        raise HTTPException(
            status_code=404,
            detail="Campaign not found"
        )

    return campaign


# -------------------------------
# UPDATE CAMPAIGN
# -------------------------------

@router.put("/campaigns/{campaign_id}")
def update_campaign(
    campaign_id: int,
    updated: CampaignUpdate,
    db: Session = Depends(get_db),
    admin: str = Depends(get_current_admin)
):

    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id
    ).first()

    if campaign is None:

        raise HTTPException(
            status_code=404,
            detail="Campaign not found"
        )

    campaign.campaign_name = updated.campaign_name
    campaign.email_subject = updated.email_subject
    campaign.email_template = updated.email_template
    campaign.difficulty = updated.difficulty
    campaign.status = updated.status

    db.commit()

    return {
        "message": "Campaign updated successfully"
    }
# -------------------------------
# UPDATE CAMPAIGN STATUS
# -------------------------------

@router.put("/campaigns/{campaign_id}/status")
def update_campaign_status(
    campaign_id: int,
    status: str,
    db: Session = Depends(get_db),
    admin: str = Depends(get_current_admin)
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


# -------------------------------
# SCHEDULE CAMPAIGN
# -------------------------------

@router.put("/campaigns/{campaign_id}/schedule")
def schedule_campaign(
    campaign_id: int,
    schedule: CampaignSchedule,
    db: Session = Depends(get_db),
    
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
        "status": campaign.status,
        "start_date": campaign.start_date,
        "end_date": campaign.end_date
    }
# -------------------------------
# COMPLETE CAMPAIGN
# -------------------------------

@router.post("/campaigns/{campaign_id}/complete")
def complete_campaign(
    campaign_id: int,
    db: Session = Depends(get_db),
):

    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id
    ).first()

    if campaign is None:
        raise HTTPException(
            status_code=404,
            detail="Campaign not found"
        )

    if campaign.status != "Running":
        raise HTTPException(
            status_code=400,
            detail="Only running campaigns can be completed."
        )

    campaign.status = "Completed"

    campaign.end_date = datetime.now(
        ZoneInfo("Asia/Kolkata")
    )

    db.commit()

    return {
        "message": "Campaign completed successfully",
        "status": campaign.status
    }

# -------------------------------
# CAMPAIGN ANALYTICS
# -------------------------------

@router.get("/campaigns/{campaign_id}/analytics")
def campaign_analytics(
    campaign_id: int,
    db: Session = Depends(get_db),
    admin: str = Depends(get_current_admin)
):

    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id
    ).first()

    if campaign is None:
        raise HTTPException(
            status_code=404,
            detail="Campaign not found"
        )

    emails_sent = db.query(Employee).count()

    emails_opened = db.query(ClickLog).filter(
        ClickLog.campaign_id == campaign_id
    ).count()

    link_clicks = db.query(ClickLog).filter(
        ClickLog.campaign_id == campaign_id
    ).count()

    submitted = db.query(Employee).filter(
        Employee.submitted_credentials == True
    ).count()

    click_rate = 0

    if emails_sent > 0:
        click_rate = round(
            (link_clicks / emails_sent) * 100,
            2
        )

    return {
        "campaign_id": campaign.id,
        "campaign_name": campaign.campaign_name,
        "emails_sent": emails_sent,
        "emails_opened": emails_opened,
        "link_clicks": link_clicks,
        "credentials_submitted": submitted,
        "click_rate": click_rate
    }


# -------------------------------
# DEPARTMENT ANALYTICS
# -------------------------------

@router.get("/campaigns/departments/analytics")
def department_analytics(
    db: Session = Depends(get_db),
    admin: str = Depends(get_current_admin)
):

    departments = db.query(
        Employee.department
    ).distinct().all()

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

        risk = 0

        if total > 0:
            risk = round(
                (clicked / total) * 100,
                2
            )

        result.append({

            "department": department,

            "employees": total,

            "clicked": clicked,

            "submitted_credentials": submitted,

            "risk_score": risk

        })

    return result
@router.post("/campaigns/{campaign_id}/attachment")
async def upload_campaign_attachment(
    campaign_id: int,
    attachment: UploadFile = File(...),
    db: Session = Depends(get_db),
    admin: str = Depends(get_current_admin)
):

    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id
    ).first()

    if campaign is None:
        raise HTTPException(
            status_code=404,
            detail="Campaign not found"
        )

    allowed_extensions = {
        ".pdf",
        ".doc",
        ".docx",
        ".xls",
        ".xlsx",
        ".ppt",
        ".pptx",
        ".png",
        ".jpg",
        ".jpeg",
        ".zip"
    }

    extension = os.path.splitext(
        attachment.filename
    )[1].lower()

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Unsupported attachment type"
        )

    upload_dir = os.path.join(
        "uploads",
        "attachments"
    )

    os.makedirs(
        upload_dir,
        exist_ok=True
    )

    unique_filename = (
        f"{uuid.uuid4()}{extension}"
    )

    file_path = os.path.join(
        upload_dir,
        unique_filename
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            attachment.file,
            buffer
        )

    campaign.attachment_name = attachment.filename
    campaign.attachment_path = file_path
    campaign.attachment_type = attachment.content_type

    campaign.attachment_size = os.path.getsize(
        file_path
    )

    db.commit()

    return {

        "message": "Attachment uploaded successfully",

        "attachment_name": campaign.attachment_name,

        "attachment_size": campaign.attachment_size,

        "attachment_type": campaign.attachment_type

    }

# -------------------------------
# DELETE CAMPAIGN
# -------------------------------

@router.delete("/campaigns/{campaign_id}")
def delete_campaign(
    campaign_id: int,
    db: Session = Depends(get_db),
    admin: str = Depends(get_current_admin)
):

    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id
    ).first()

    if campaign is None:
        raise HTTPException(
            status_code=404,
            detail="Campaign not found"
        )

    db.delete(campaign)
    db.commit()

    return {
        "message": "Campaign deleted successfully"
    }


