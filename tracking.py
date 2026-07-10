from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime

from database import get_db
from tracking_models import ClickLog

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/track/{employee_id}/{campaign_id}")
def track_click(
    request: Request,
    employee_id: int,
    campaign_id: int,
    db: Session = Depends(get_db)
):

    # Get client IP
    ip = request.client.host

    click = ClickLog(
        employee_id=employee_id,
        campaign_id=campaign_id,
        clicked_time=datetime.now(),
        ip_address=ip
    )

    db.add(click)
    db.commit()

    return templates.TemplateResponse(
    request=request,
    name="awareness.html",
    context={}
)