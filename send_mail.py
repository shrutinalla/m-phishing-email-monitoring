'''from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from database import get_db
from models import Employee
from campaign_models import Campaign
from template_models import EmailTemplate
from email_service import send_phishing_email

router = APIRouter()


@router.post("/send-campaign/{campaign_id}")
async def send_campaign(
    campaign_id: int,
    db: Session = Depends(get_db)
):

    # Get campaign
    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id
    ).first()

    if campaign is None:
        raise HTTPException(
            status_code=404,
            detail="Campaign not found"
        )

    # Get email template linked to campaign
    template = db.query(EmailTemplate).filter(
        EmailTemplate.id == campaign.template_id
    ).first()

    if template is None:
        raise HTTPException(
            status_code=404,
            detail="Email template not found"
        )

    # Get all employees
    employees = db.query(Employee).all()

    if not employees:
        raise HTTPException(
            status_code=404,
            detail="No employees found"
        )

    sent = 0
    failed = 0

    for emp in employees:

        # Subject comes from template
        subject = template.subject

        # HTML comes from template
        body = template.content

        # Replace placeholders
        body = body.replace(
            "{employee_name}",
            emp.name
        )

        body = body.replace(
            "{employee_email}",
            emp.email
        )

        body = body.replace(
            "{tracking_link}",
            f"http://127.0.0.1:8000/track/{emp.id}/{campaign.id}"
        )
        body = body.replace("{campaign_name}", campaign.campaign_name)
        body = body.replace("{company_name}", "MIDHANI")
        body = body.replace("{current_date}", datetime.now().strftime("%d-%m-%Y"))

        try:

            await send_phishing_email(
                recipient_email=emp.email,
                subject=subject,
                body=body
            )

            sent += 1

        except Exception as e:

            failed += 1

            print(f"Failed to send email to {emp.email}")
            print(e)

    campaign.status = "Running"
    campaign.start_date = datetime.utcnow()

    db.commit()

    return {

        "message": "Campaign execution completed",

        "campaign_id": campaign.id,

        "campaign_name": campaign.campaign_name,

        "template_used": template.template_name,

        "emails_sent": sent,

        "emails_failed": failed,

        "total_employees": len(employees),

        "status": campaign.status

    }'''

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from database import get_db

from models import Employee
from campaign_models import Campaign
from template_models import EmailTemplate

from email_service import send_phishing_email
from email_log_models import EmailLog

from audit_models import AuditLog


router = APIRouter(
    prefix="/mail",
    tags=["Email Sending"]
)


@router.post("/send-campaign/{campaign_id}")
async def send_campaign(
    campaign_id: int,
    db: Session = Depends(get_db)
):

    # --------------------------
    # Get Campaign
    # --------------------------

    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id
    ).first()


    if campaign is None:
        raise HTTPException(
            status_code=404,
            detail="Campaign not found"
        )


    # --------------------------
    # Get Template
    # --------------------------

    template = db.query(EmailTemplate).filter(
        EmailTemplate.id == campaign.template_id
    ).first()


    if template is None:
        raise HTTPException(
            status_code=404,
            detail="Email template not found"
        )


    # --------------------------
    # Get Employees
    # --------------------------

    employees = db.query(Employee).all()


    if not employees:
        raise HTTPException(
            status_code=404,
            detail="No employees found"
        )


    sent = 0
    failed = 0


    # --------------------------
    # Send Emails
    # --------------------------

    for emp in employees:

        subject = template.subject

        body = template.content


        body = body.replace(
            "{employee_name}",
            emp.name
        )

        body = body.replace(
            "{employee_email}",
            emp.email
        )

        body = body.replace(
            "{tracking_link}",
            f"http://127.0.0.1:8000/track/{emp.id}/{campaign.id}"
        )

        body = body.replace(
            "{campaign_name}",
            campaign.campaign_name
        )

        body = body.replace(
            "{company_name}",
            "MIDHANI"
        )

        body = body.replace(
            "{current_date}",
            datetime.now().strftime("%d-%m-%Y")
        )


        try:

            await send_phishing_email(
                recipient_email=emp.email,
                subject=subject,
                body=body
            )


            email_log = EmailLog(
                employee_id=emp.id,
                campaign_id=campaign.id,
                email=emp.email,
                status="Sent"
            )


            db.add(email_log)
            db.commit()


            sent += 1



        except Exception as e:


            email_log = EmailLog(
                employee_id=emp.id,
                campaign_id=campaign.id,
                email=emp.email,
                status="Failed",
                error_message=str(e)
            )


            db.add(email_log)
            db.commit()


            failed += 1

            print(e)



    # --------------------------
    # Update Campaign
    # --------------------------

    campaign.status = "Running"

    campaign.start_date = datetime.utcnow()

    campaign.emails_sent = sent

    campaign.emails_failed = failed

    campaign.total_recipients = len(employees)


    db.commit()



    # --------------------------
    # Create Audit Log
    # --------------------------

    log = AuditLog(
        action="Campaign Sent",
        performed_by="Admin",
        module="Campaign",
        details=f"Campaign '{campaign.campaign_name}' sent to {sent} employees",
        timestamp=datetime.utcnow()
    )


    db.add(log)

    db.commit()



    # --------------------------
    # Response
    # --------------------------

    return {

        "message": "Campaign execution completed",

        "campaign_id": campaign.id,

        "campaign_name": campaign.campaign_name,

        "template_used": template.template_name,

        "emails_sent": sent,

        "emails_failed": failed,

        "total_employees": len(employees),

        "status": campaign.status

    }