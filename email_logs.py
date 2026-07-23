from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from email_log_models import EmailLog


router = APIRouter(
    prefix="/email-logs",
    tags=["Email Logs"]
)



@router.get("/")
def get_email_logs(
    db: Session = Depends(get_db)
):

    logs = db.query(
        EmailLog
    ).all()


    return logs