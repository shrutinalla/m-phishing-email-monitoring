from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi.responses import RedirectResponse
from database import get_db
from tracking_models import ClickLog
from models import Employee

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
    user_agent = request.headers.get("user-agent")

    click = ClickLog(
    employee_id=employee_id,
    campaign_id=campaign_id,
    clicked_time=datetime.now(),
    ip_address=ip,
    user_agent=user_agent
)

    db.add(click)
    employee = (    
        db.query(Employee)
        .filter(Employee.id == employee_id)
        .first()
        )
    if employee:
        employee.clicked = True
    db.commit()

    return RedirectResponse(
    url="http://localhost:5173/warning",
    status_code=302
)