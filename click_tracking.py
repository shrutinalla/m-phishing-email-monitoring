from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from database import get_db
from tracking_models import ClickLog


router = APIRouter()


@router.get("/track/{employee_id}/{campaign_id}")
def track_click(
    employee_id: int,
    campaign_id: int,
    db: Session = Depends(get_db)
):

    click = ClickLog(
        employee_id=employee_id,
        campaign_id=campaign_id,
        clicked_at=datetime.utcnow()
    )

    db.add(click)
    db.commit()
    db.refresh(click)


    return {
        "message": "Click recorded successfully",
        "employee_id": employee_id,
        "campaign_id": campaign_id
    }