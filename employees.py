from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from pydantic import BaseModel

from database import get_db
from models import Employee

router = APIRouter()


class EmployeeCreate(BaseModel):
    name: str
    email: str
    department: str


@router.post("/employees")
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):

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


@router.get("/employees")
def get_employees(db: Session = Depends(get_db)):

    return db.query(Employee).all()

@router.get("/employees/department/{department}")
def get_department_employees(
    department: str,
    db: Session = Depends(get_db)
):

    employees = db.query(Employee).filter(
        Employee.department.ilike(department)
    ).all()

    return employees

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
@router.put("/employees/{employee_id}")
def update_employee(
    employee_id: int,
    clicked: bool,
    submitted_credentials: bool,
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

    employee.clicked = clicked
    employee.submitted_credentials = submitted_credentials

    db.commit()

    return {
        "message": "Employee updated successfully"
    }
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


@router.delete("/employees/{employee_id}")
def delete_employee(
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

    db.delete(employee)
    db.commit()

    return {
        "message": "Employee deleted successfully"
    }
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