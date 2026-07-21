from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Employee
from schemas import EmployeeCreate

from campaign_models import Campaign
from campaign_schemas import CampaignCreate, CampaignUpdate
from template_models import EmailTemplate
from template_schemas import TemplateCreate
from tracking import router as tracking_router
from send_mail import router as mail_router
from reports import router as reports_router
from employees import router as employee_router
from employee_upload import router as upload_router
from employee_pdf import router as pdf_router
from campaigns import router as campaign_router
from campaign_pdf import router as campaign_pdf_router


app = FastAPI()

app.include_router(tracking_router)
app.include_router(mail_router)
app.include_router(reports_router)
app.include_router(employee_router)
app.include_router(upload_router)
app.include_router(pdf_router)
app.include_router(campaign_router)
app.include_router(campaign_pdf_router)

@app.get("/")
def home():
    return {"message": "Phishing Awareness System API Running"}


@app.post("/templates")
def create_template(
    template: TemplateCreate,
    db: Session = Depends(get_db)
):

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


@app.get("/templates")
def get_templates(db: Session = Depends(get_db)):
    return db.query(EmailTemplate).all()