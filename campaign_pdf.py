from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from database import get_db
from campaign_models import Campaign

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle
)

from reportlab.lib import colors

router = APIRouter()


@router.get("/campaigns/report/pdf")
def campaign_pdf(db: Session = Depends(get_db)):

    campaigns = db.query(Campaign).all()

    filename = "campaign_report.pdf"

    pdf = SimpleDocTemplate(filename)

    data = [[
        "ID",
        "Campaign",
        "Subject",
        "Difficulty",
        "Status"
    ]]

    for campaign in campaigns:

        data.append([
            campaign.id,
            campaign.campaign_name,
            campaign.email_subject,
            campaign.difficulty,
            campaign.status
        ])

    table = Table(data)

    table.setStyle(TableStyle([

        ("BACKGROUND",(0,0),(-1,0),colors.darkblue),

        ("TEXTCOLOR",(0,0),(-1,0),colors.white),

        ("GRID",(0,0),(-1,-1),1,colors.black),

        ("BACKGROUND",(0,1),(-1,-1),colors.beige),

        ("ALIGN",(0,0),(-1,-1),"CENTER"),

        ("BOTTOMPADDING",(0,0),(-1,0),10)

    ]))

    pdf.build([table])

    return FileResponse(
        filename,
        media_type="application/pdf",
        filename=filename
    )