from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Employee
from schemas import EmployeeCreate

from campaign_models import Campaign
from campaign_schemas import CampaignCreate
from template_models import EmailTemplate
from template_schemas import TemplateCreate
from tracking import router as tracking_router
from send_mail import router as mail_router
from reports import router as reports_router
from employees import router as employee_router
from employee_upload import router as upload_router

app = FastAPI()

app.include_router(tracking_router)
app.include_router(mail_router)
app.include_router(reports_router)
app.include_router(employee_router)
app.include_router(upload_router)
@app.get("/")
def home():
    return {"message": "Phishing Awareness System API Running"}




# @app.put("/employees/{employee_id}")
# def update_employee(
#     employee_id: int,
#     clicked: bool,
#     submitted_credentials: bool,
#     db: Session = Depends(get_db)
# ):

#     employee = db.query(Employee).filter(
#         Employee.id == employee_id
#     ).first()

#     if not employee:
#         return {"message": "Employee not found"}

#     employee.clicked = clicked
#     employee.submitted_credentials = submitted_credentials

#     db.commit()

#     return {
#         "message": "Employee updated successfully"
#     }
@app.post("/campaigns")
def create_campaign(
    campaign: CampaignCreate,
    db: Session = Depends(get_db)
):

    new_campaign = Campaign(
        campaign_name=campaign.campaign_name,
        email_subject=campaign.email_subject,
        email_template=campaign.email_template
    )

    db.add(new_campaign)
    db.commit()
    db.refresh(new_campaign)

    return {
        "message": "Campaign created successfully",
        "campaign_id": new_campaign.id
    }


@app.get("/campaigns")
def get_campaigns(db: Session = Depends(get_db)):
    return db.query(Campaign).all()
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