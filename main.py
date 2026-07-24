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
from campaign_export import router as campaign_export_router
from campaign_history import router as campaign_history_router
from risk import router as risk_router
from risk_pdf import router as risk_pdf_router
from risk_excel import router as risk_excel_router
from admin_auth import router as admin_router
from templates import router as template_router
from fastapi import BackgroundTasks
from email_sender import send_phishing_email
from analytics import router as analytics_router
from email_logs import router as email_logs_router
from live_tracking import router as live_tracking_router
from dashboard import router as dashboard_router
from notifications import router as notification_router
from audit_logs import router as audit_router

app = FastAPI()

app.include_router(tracking_router)
app.include_router(reports_router)
app.include_router(employee_router)
app.include_router(upload_router)
app.include_router(pdf_router)
app.include_router(campaign_router)
app.include_router(campaign_pdf_router)
app.include_router(campaign_export_router)
app.include_router(campaign_history_router)
app.include_router(risk_router)
app.include_router(risk_pdf_router)
app.include_router(risk_excel_router)
app.include_router(admin_router)
app.include_router(template_router)
app.include_router(analytics_router)
app.include_router(mail_router)
app.include_router(email_logs_router)
app.include_router(live_tracking_router)
app.include_router(dashboard_router)
app.include_router(notification_router)
app.include_router(audit_router)

@app.get("/")
def home():
    return {"message": "Phishing Awareness System API Running"}


@app.post("/test-email")
async def test_email(background_tasks: BackgroundTasks):

    background_tasks.add_task(
        send_phishing_email,
        "shrutin011004@gmail.com",
        "Testing Email",
        "<h2>Hello from MIDHANI</h2>"
    )

    return {
        "message": "Email sent"
    }