from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from openpyxl import Workbook

from database import get_db
from campaign_models import Campaign

router = APIRouter()


@router.get("/campaigns/export/excel")
def export_campaigns(db: Session = Depends(get_db)):

    campaigns = db.query(Campaign).all()

    wb = Workbook()
    ws = wb.active

    ws.title = "Campaign Report"

    ws.append([
        "ID",
        "Campaign Name",
        "Subject",
        "Difficulty",
        "Status",
        "Created At",
        "Start Date",
        "End Date"
    ])

    for c in campaigns:

        ws.append([
            c.id,
            c.campaign_name,
            c.email_subject,
            c.difficulty,
            c.status,
            c.created_at,
            c.start_date,
            c.end_date
        ])

    filename = "campaign_report.xlsx"

    wb.save(filename)

    return FileResponse(
        filename,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=filename
    )