'''from fastapi import APIRouter, Depends, HTTPException
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

        print("=" * 60)
        print("Employee :", emp.name)
        print("Email    :", emp.email)
        print("=" * 60)

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

            print("SUCCESS:", emp.email)

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

            print("FAILED:", emp.email)
            print("ERROR :", e)

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
    # Audit Log
    # --------------------------

    audit = AuditLog(
        action="Campaign Sent",
        performed_by="Admin",
        module="Campaign",
        details=f"Campaign '{campaign.campaign_name}' sent to {sent} employees",
        timestamp=datetime.utcnow()
    )

    db.add(audit)
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

    print("\n" + "=" * 70)
    print("SEND CAMPAIGN REQUEST")
    print("=" * 70)
    print("Campaign ID Received:", campaign_id)

    # --------------------------
    # Get Campaign
    # --------------------------

    print("\nSearching campaign...")

    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id
    ).first()

    print("Campaign =", campaign)

    if campaign is None:
        raise HTTPException(
            status_code=404,
            detail="Campaign not found"
        )

    print("Campaign Name :", campaign.campaign_name)
    print("Template ID   :", campaign.template_id)

    # --------------------------
    # Get Template
    # --------------------------

    print("\nSearching template...")

    template = db.query(EmailTemplate).filter(
        EmailTemplate.id == campaign.template_id
    ).first()

    print("Template =", template)

    if template is None:
        raise HTTPException(
            status_code=404,
            detail="Email template not found"
        )

    print("Template Name :", template.template_name)

    # --------------------------
    # Get Employees
    # --------------------------

    employees = db.query(Employee).all()

    print("Employees Found =", len(employees))

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

        print("\n" + "=" * 60)
        print("Employee :", emp.name)
        print("Email    :", emp.email)
        print("=" * 60)

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

            print("SUCCESS:", emp.email)

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

            print("FAILED :", emp.email)
            print("ERROR  :", e)

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
    # Audit Log
    # --------------------------

    audit = AuditLog(
        action="Campaign Sent",
        performed_by="Admin",
        module="Campaign",
        details=f"Campaign '{campaign.campaign_name}' sent to {sent} employees",
        timestamp=datetime.utcnow()
    )

    db.add(audit)
    db.commit()

    print("\nCampaign Execution Completed")
    print("Emails Sent   :", sent)
    print("Emails Failed :", failed)

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