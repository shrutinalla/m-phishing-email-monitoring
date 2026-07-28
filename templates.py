
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_

from database import get_db
from template_models import EmailTemplate
from template_schemas import TemplateCreate
from campaign_models import Campaign
from auth_dependency import get_current_admin
from audit_models import AuditLog
from datetime import datetime
from zoneinfo import ZoneInfo

router = APIRouter()


# -----------------------------
# CREATE TEMPLATE
# -----------------------------
@router.post("/templates")
def create_template(
    template: TemplateCreate,
    db: Session = Depends(get_db)
):
    existing = db.query(EmailTemplate).filter(
        EmailTemplate.template_name == template.template_name
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Template already exists"
        )

    new_template = EmailTemplate(
        template_name=template.template_name,
        subject=template.subject,
        content=template.content
    )

    db.add(new_template)
    db.commit()
    db.refresh(new_template)
     # -----------------------------
# Audit Log
# -----------------------------

    log = AuditLog(
    action="Template Created",
    performed_by="Developer",
    module="Template",
    details=f"Template '{new_template.template_name}' created",
    timestamp=datetime.now(ZoneInfo("Asia/Kolkata"))
)
    db.add(log)
    db.commit()

    return {
    "message": "Template created successfully",
    "template": {
        "id": new_template.id,
        "template_name": new_template.template_name,
        "subject": new_template.subject
    }
}


# -----------------------------
# GET ALL TEMPLATES
# -----------------------------
@router.get("/templates")
def get_templates(
    db: Session = Depends(get_db)
):
    templates = db.query(EmailTemplate).all()

    result = []

    for template in templates:

        campaign_count = db.query(Campaign).filter(
            Campaign.template_id == template.id
        ).count()

        result.append(
            {
                "id": template.id,
                "template_name": template.template_name,
                "subject": template.subject,
                "content": template.content,
                "campaign_count": campaign_count
            }
        )

    return result
# -----------------------------
# TEMPLATE DROPDOWN
# -----------------------------
@router.get("/templates/list")
def template_list(
    db: Session = Depends(get_db)
):
    templates = db.query(EmailTemplate).all()

    return [
        {
            "id": t.id,
            "template_name": t.template_name
        }
        for t in templates
    ]


# -----------------------------
# SEARCH TEMPLATE
# -----------------------------
@router.get("/templates/search")
def search_templates(
    keyword: str,
    db: Session = Depends(get_db)
):
    return db.query(EmailTemplate).filter(
        or_(
            EmailTemplate.template_name.ilike(f"%{keyword}%"),
            EmailTemplate.subject.ilike(f"%{keyword}%"),
            EmailTemplate.content.ilike(f"%{keyword}%")
        )
    ).all()


# -----------------------------
# PREVIEW TEMPLATE
# -----------------------------
@router.get("/templates/{template_id}/preview")
def preview_template(
    template_id: int,
    db: Session = Depends(get_db)
):

    template = db.query(EmailTemplate).filter(
        EmailTemplate.id == template_id
    ).first()

    if template is None:
        raise HTTPException(
            status_code=404,
            detail="Template not found"
        )

    return {
        "template_name": template.template_name,
        "subject": template.subject,
        "content": template.content
    }


# -----------------------------
# CAMPAIGNS USING TEMPLATE
# -----------------------------
@router.get("/templates/{template_id}/campaigns")
def template_campaigns(
    template_id: int,
    db: Session = Depends(get_db)
):
    return db.query(Campaign).filter(
        Campaign.template_id == template_id
    ).all()


# -----------------------------
# GET TEMPLATE BY ID
# -----------------------------
@router.get("/templates/{template_id}")
def get_template(
    template_id: int,
    db: Session = Depends(get_db)
):

    template = db.query(EmailTemplate).filter(
        EmailTemplate.id == template_id
    ).first()

    if template is None:
        raise HTTPException(
            status_code=404,
            detail="Template not found"
        )

    return template


# -----------------------------
# UPDATE TEMPLATE
# -----------------------------
@router.put("/templates/{template_id}")
def update_template(
    template_id: int,
    updated: TemplateCreate,
    db: Session = Depends(get_db)
):

    template = db.query(EmailTemplate).filter(
        EmailTemplate.id == template_id
    ).first()

    if template is None:
        raise HTTPException(
            status_code=404,
            detail="Template not found"
        )

    template.template_name = updated.template_name
    template.subject = updated.subject
    template.content = updated.content

    db.commit()

    return {
        "message": "Template updated successfully"
    }


# -----------------------------
# DELETE TEMPLATE
# -----------------------------
@router.delete("/templates/{template_id}")
def delete_template(
    template_id: int,
    db: Session = Depends(get_db)
):

    template = db.query(EmailTemplate).filter(
        EmailTemplate.id == template_id
    ).first()

    if template is None:
        raise HTTPException(
            status_code=404,
            detail="Template not found"
        )

    db.delete(template)
    db.commit()

    return {
        "message": "Template deleted successfully"
    }