from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from pydantic import BaseModel
from fastapi.responses import FileResponse
from openpyxl import Workbook
from datetime import datetime
from campaign_models import Campaign

from tracking_models import ClickLog
from auth_dependency import get_current_admin
from database import get_db
from models import Employee
from audit_models import AuditLog


router = APIRouter()


class EmployeeCreate(BaseModel):
    name: str
    email: str
    department: str


class EmployeeUpdate(BaseModel):
    name: str
    email: str
    department: str



# -----------------------------
# Add Employee
# -----------------------------
@router.post("/employees")
def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db),
):

    emp = Employee(
        name=employee.name,
        email=employee.email,
        department=employee.department
    )

    db.add(emp)
    db.commit()
    db.refresh(emp)

    return {
        "message": "Employee added successfully",
        "employee_id": emp.id
    }



# -----------------------------
# Get All Employees
# -----------------------------
@router.get("/employees")
def get_employees(
    db: Session = Depends(get_db)
):

    return db.query(Employee).all()



# -----------------------------
# Get Employees By Department
# -----------------------------
@router.get("/employees/department/{department}")
def get_department_employees(
    department: str,
    db: Session = Depends(get_db)
):

    employees = db.query(Employee).filter(
        Employee.department.ilike(department)
    ).all()

    return employees



# -----------------------------
# Employee Statistics
# -----------------------------
@router.get("/employees/statistics")
def employee_statistics(
    db: Session = Depends(get_db)
):

    total = db.query(Employee).count()

    clicked = db.query(Employee).filter(
        Employee.clicked == True
    ).count()

    submitted = db.query(Employee).filter(
        Employee.submitted_credentials == True
    ).count()

    safe = total - clicked


    return {

        "total_employees": total,

        "clicked_phishing_link": clicked,

        "submitted_credentials": submitted,

        "safe_employees": safe

    }



# -----------------------------
# Employee Dashboard
# -----------------------------
@router.get("/employees/dashboard")
def employee_dashboard(
    db: Session = Depends(get_db)
):

    # Employee Statistics
    total = db.query(Employee).count()

    clicked = db.query(Employee).filter(
        Employee.clicked == True
    ).count()

    submitted = db.query(Employee).filter(
        Employee.submitted_credentials == True
    ).count()

    high = submitted

    medium = db.query(Employee).filter(
        Employee.clicked == True,
        Employee.submitted_credentials == False
    ).count()

    low = total - high - medium

    # Campaign Statistics
    total_campaigns = db.query(Campaign).count()

    running_campaigns = (
        db.query(Campaign)
        .filter(Campaign.status == "Running")
        .count()
    )

    completed_campaigns = (
        db.query(Campaign)
        .filter(Campaign.status == "Completed")
        .count()
    )

    campaigns = db.query(Campaign).all()

    emails_sent = sum(
        campaign.emails_sent or 0
        for campaign in campaigns
    )

    emails_failed = sum(
        campaign.emails_failed or 0
        for campaign in campaigns
    )

    total_clicks = db.query(ClickLog).count()

    click_rate = (
        round((total_clicks / emails_sent) * 100, 2)
        if emails_sent > 0
        else 0
    )

    return {
        "total_employees": total,
        "clicked": clicked,
        "submitted_credentials": submitted,
        "safe": low,
        "high_risk": high,
        "medium_risk": medium,
        "low_risk": low,

        "total_campaigns": total_campaigns,
        "running_campaigns": running_campaigns,
        "completed_campaigns": completed_campaigns,
        "emails_sent": emails_sent,
        "emails_failed": emails_failed,
        "total_clicks": total_clicks,
        "click_rate": click_rate
    }

# -----------------------------
# Employee Risk
# -----------------------------
@router.get("/employees/risk/{employee_id}")
def employee_risk(
    employee_id: int,
    db: Session = Depends(get_db)
):

    employee = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()


    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )


    if employee.submitted_credentials:
        risk = "High"

    elif employee.clicked:
        risk = "Medium"

    else:
        risk = "Low"


    return {

        "employee_id": employee.id,

        "name": employee.name,

        "department": employee.department,

        "risk_level": risk

    }



# -----------------------------
# Employee Profile
# -----------------------------
@router.get("/employees/profile/{employee_id}")
def employee_profile(
    employee_id: int,
    db: Session = Depends(get_db)
):

    employee = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()


    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )


    if employee.submitted_credentials:
        risk = "High"

    elif employee.clicked:
        risk = "Medium"

    else:
        risk = "Low"


    return {

        "employee_id": employee.id,

        "name": employee.name,

        "email": employee.email,

        "department": employee.department,

        "clicked": employee.clicked,

        "submitted_credentials": employee.submitted_credentials,

        "risk_level": risk

    }



# -----------------------------
# Update Employee
# -----------------------------
@router.put("/employees/{employee_id}")
def update_employee(
    employee_id: int,
    employee: EmployeeUpdate,
    db: Session = Depends(get_db),
):

    emp = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()


    if emp is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )


    emp.name = employee.name
    emp.email = employee.email
    emp.department = employee.department


    db.commit()
    db.refresh(emp)



    return {
        "message": "Employee updated successfully",
        "employee": {
            "id": emp.id,
            "name": emp.name,
            "email": emp.email,
            "department": emp.department
        }
    }



# -----------------------------
# Search Employee
# -----------------------------
@router.get("/employees/search")
def search_employee(
    keyword: str,
    db: Session = Depends(get_db)
):

    employees = db.query(Employee).filter(

        or_(

            Employee.name.ilike(f"%{keyword}%"),

            Employee.email.ilike(f"%{keyword}%"),

            Employee.department.ilike(f"%{keyword}%")

        )

    ).all()


    return employees



# -----------------------------
# Delete Employee
# -----------------------------
@router.delete("/employees/{employee_id}")
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db),
):

    employee = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()


    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )


    employee_name = employee.name


    db.delete(employee)
    db.commit()




    return {
        "message": "Employee deleted successfully"
    }



# -----------------------------
# Export Employees
# -----------------------------
@router.get("/employees/export")
def export_employees(
    db: Session = Depends(get_db)
):

    employees = db.query(Employee).all()


    workbook = Workbook()

    sheet = workbook.active


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



# -----------------------------
# Get Single Employee
# -----------------------------
@router.get("/employees/{employee_id}")
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):

    employee = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()


    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )


    return employee