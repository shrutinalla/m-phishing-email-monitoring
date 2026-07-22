from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from database import get_db
from models import Employee

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle
)

from reportlab.lib import colors

router = APIRouter()


@router.get("/risk/report/pdf")
def risk_pdf(db: Session = Depends(get_db)):

    employees = db.query(Employee).all()

    filename = "employee_risk_report.pdf"

    pdf = SimpleDocTemplate(filename)

    data = [[
        "ID",
        "Name",
        "Department",
        "Risk Score",
        "Risk Level"
    ]]

    for emp in employees:

        data.append([
            emp.id,
            emp.name,
            emp.department,
            emp.risk_score,
            emp.risk_level
        ])

    table = Table(data)

    table.setStyle(TableStyle([

        ("BACKGROUND", (0,0), (-1,0), colors.darkred),

        ("TEXTCOLOR", (0,0), (-1,0), colors.white),

        ("GRID", (0,0), (-1,-1), 1, colors.black),

        ("BACKGROUND", (0,1), (-1,-1), colors.beige),

        ("ALIGN", (0,0), (-1,-1), "CENTER"),

        ("BOTTOMPADDING", (0,0), (-1,0), 10)

    ]))

    pdf.build([table])

    return FileResponse(
        filename,
        media_type="application/pdf",
        filename=filename
    )