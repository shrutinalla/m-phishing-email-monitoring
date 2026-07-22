from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from database import get_db
from models import Employee

from openpyxl import Workbook

router = APIRouter()


@router.get("/risk/report/excel")
def risk_excel(db: Session = Depends(get_db)):

    employees = db.query(Employee).all()

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Employee Risk Report"

    sheet.append([
        "ID",
        "Name",
        "Email",
        "Department",
        "Risk Score",
        "Risk Level"
    ])

    for emp in employees:

        sheet.append([
            emp.id,
            emp.name,
            emp.email,
            emp.department,
            emp.risk_score,
            emp.risk_level
        ])

    filename = "employee_risk_report.xlsx"

    workbook.save(filename)

    return FileResponse(
        filename,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=filename
    )