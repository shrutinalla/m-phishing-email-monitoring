from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from template_models import EmailTemplate
from template_schemas import TemplateCreate

router = APIRouter()


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

    return {
        "message": "Template created successfully",
        "template_id": new_template.id
    }
@router.get("/templates")
def get_templates(
    db: Session = Depends(get_db)
):
    return db.query(EmailTemplate).all()

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