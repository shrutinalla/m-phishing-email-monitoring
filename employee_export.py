from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from database import get_db
from models import Employee

from openpyxl import Workbook

router = APIRouter()


@router.get("/employees/export")
def export_employees(
    db: Session = Depends(get_db)
):

    employees = db.query(Employee).all()

    workbook = Workbook()

    sheet = workbook.active
    sheet.title = "Employees"

    sheet.append([
        "ID",
        "Name",
        "Email",
        "Department",
        "Clicked",
        "Submitted Credentials"
    ])

    for emp in employees:

        sheet.append([
            emp.id,
            emp.name,
            emp.email,
            emp.department,
            emp.clicked,
            emp.submitted_credentials
        ])

    filename = "employees.xlsx"

    workbook.save(filename)

    return FileResponse(
        filename,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=filename
    )