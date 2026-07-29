from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from zoneinfo import ZoneInfo

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
    print("Campaign ID:", campaign_id)

    # ---------------------------------
    # Get Campaign
    # ---------------------------------

    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id
    ).first()

    if campaign is None:
        raise HTTPException(
            status_code=404,
            detail="Campaign not found"
        )

    print("Campaign:", campaign.campaign_name)
    print("Template ID:", campaign.template_id)

    # ---------------------------------
    # Load Template (Optional)
    # ---------------------------------

    template = None

    if campaign.template_id is not None:

        template = db.query(EmailTemplate).filter(
            EmailTemplate.id == campaign.template_id
        ).first()

        if template is None:
            raise HTTPException(
                status_code=404,
                detail="Email template not found"
            )

        print("Using template:", template.template_name)

    else:

        print("Using custom campaign content")

    # ---------------------------------
    # Employees
    # ---------------------------------

    employees = db.query(Employee).all()

    if not employees:
        raise HTTPException(
            status_code=404,
            detail="No employees found"
        )

    sent = 0
    failed = 0

    # ---------------------------------
    # Send Emails
    # ---------------------------------

    for emp in employees:

        if template:

            subject = template.subject
            body = template.content

        else:

            subject = campaign.email_subject
            body = campaign.email_template

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
                body=body,
                attachment_path=campaign.attachment_path,
                attachment_name=campaign.attachment_name
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

            print("SUCCESS:", emp.email)

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

            print("FAILED:", emp.email)
            print(e)

    # ---------------------------------
    # Update Campaign
    # ---------------------------------

    campaign.status = "Running"
    campaign.start_date = datetime.now(
        ZoneInfo("Asia/Kolkata")
    )

    campaign.total_recipients = len(employees)
    campaign.emails_sent = sent
    campaign.emails_failed = failed

    db.commit()

    # ---------------------------------
    # Audit Log
    # ---------------------------------

    audit = AuditLog(
        action="Campaign Sent",
        performed_by="Admin",
        module="Campaign",
        details=f"Campaign '{campaign.campaign_name}' sent to {sent} employees",
        timestamp=datetime.now(
            ZoneInfo("Asia/Kolkata")
        )
    )

    db.add(audit)
    db.commit()

    print("\nCampaign completed")

    return {
        "message": "Campaign execution completed",
        "campaign_id": campaign.id,
        "campaign_name": campaign.campaign_name,
        "template_used": (
            template.template_name
            if template
            else "Custom Email"
        ),
        "emails_sent": sent,
        "emails_failed": failed,
        "total_employees": len(employees),
        "status": campaign.status
    }
@router.post("/complete-campaign/{campaign_id}")
def complete_campaign(
    campaign_id: int,
    db: Session = Depends(get_db)
):

    campaign = (
        db.query(Campaign)
        .filter(Campaign.id == campaign_id)
        .first()
    )

    if campaign is None:
        raise HTTPException(
            status_code=404,
            detail="Campaign not found"
        )

    campaign.status = "Completed"
    campaign.end_date = datetime.now(
        ZoneInfo("Asia/Kolkata")
    )

    db.commit()

    audit = AuditLog(
        action="Campaign Completed",
        performed_by="Admin",
        module="Campaign",
        details=f"Campaign '{campaign.campaign_name}' marked as Completed",
        timestamp=datetime.now(
            ZoneInfo("Asia/Kolkata")
        )
    )

    db.add(audit)
    db.commit()

    return {
        "message": "Campaign marked as completed."
    }