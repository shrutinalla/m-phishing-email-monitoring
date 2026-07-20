from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

from database import get_db
from models import Employee

router = APIRouter()


@router.get("/employees/export/pdf")
def export_pdf(db: Session = Depends(get_db)):

    employees = db.query(Employee).all()

    filename = "employees_report.pdf"

    pdf = SimpleDocTemplate(filename)

    data = [[
        "ID",
        "Name",
        "Email",
        "Department",
        "Clicked",
        "Submitted"
    ]]

    for emp in employees:
        data.append([
            emp.id,
            emp.name,
            emp.email,
            emp.department,
            str(emp.clicked),
            str(emp.submitted_credentials)
        ])

    table = Table(data)

    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.grey),
        ("TEXTCOLOR", (0,0), (-1,0), colors.whitesmoke),
        ("GRID", (0,0), (-1,-1), 1, colors.black),
        ("BACKGROUND", (0,1), (-1,-1), colors.beige),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
    ]))

    pdf.build([table])

    return FileResponse(
        filename,
        media_type="application/pdf",
        filename=filename
    )