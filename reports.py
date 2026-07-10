from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from tracking_models import ClickLog

router = APIRouter()

@router.get("/reports")
def get_reports(db: Session = Depends(get_db)):

    logs = db.query(ClickLog).all()

    return logs