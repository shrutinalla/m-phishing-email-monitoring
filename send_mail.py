from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Employee
from email_service import send_phishing_email

router = APIRouter()


@router.post("/send-campaign/{campaign_id}")
def send_campaign(
    campaign_id: int,
    db: Session = Depends(get_db)
):

    employees = db.query(Employee).all()

    for emp in employees:

        send_phishing_email(
            emp.email,
            emp.id,
            campaign_id
        )

    return {
        "message": "Campaign sent successfully"
    }