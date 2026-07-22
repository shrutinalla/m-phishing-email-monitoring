from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from database import get_db
from models import Employee
from tracking_models import ClickLog

router = APIRouter()


@router.post("/risk/calculate")
def calculate_risk(db: Session = Depends(get_db)):

    employees = db.query(Employee).all()

    for employee in employees:

        score = 0

        # Count clicks
        click_count = db.query(ClickLog).filter(
            ClickLog.employee_id == employee.id
        ).count()

        score += click_count * 20

        # Check credential submission
        if hasattr(employee, "submitted_credentials"):
            if employee.submitted_credentials:
                score += 50

        employee.risk_score = score

        if score >= 80:
            employee.risk_level = "Critical"
        elif score >= 50:
            employee.risk_level = "High"
        elif score >= 20:
            employee.risk_level = "Medium"
        else:
            employee.risk_level = "Low"

    db.commit()

    return {
        "message": "Risk scores calculated successfully"
    }

@router.get("/risk/profile/{employee_id}")
def employee_risk_profile(
    employee_id: int,
    db: Session = Depends(get_db)
):

    employee = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()

    if employee is None:
        return {"message": "Employee not found"}

    total_clicks = db.query(ClickLog).filter(
        ClickLog.employee_id == employee.id
    ).count()

    return {
        "employee_id": employee.id,
        "name": employee.name,
        "email": employee.email,
        "department": employee.department,
        "risk_score": employee.risk_score,
        "risk_level": employee.risk_level,
        "total_clicks": total_clicks
    }

@router.get("/risk/departments")
def department_risk(
    db: Session = Depends(get_db)
):

    result = (
        db.query(
            Employee.department,
            func.avg(Employee.risk_score).label("average_risk_score"),
            func.count(Employee.id).label("employees")
        )
        .group_by(Employee.department)
        .order_by(func.avg(Employee.risk_score).desc())
        .all()
    )

    return [
        {
            "department": row.department,
            "average_risk_score": round(row.average_risk_score, 2),
            "employees": row.employees
        }
        for row in result
    ]


@router.get("/risk/top-employees")
def top_risky_employees(
    limit: int = 10,
    db: Session = Depends(get_db)
):

    employees = (
        db.query(Employee)
        .order_by(Employee.risk_score.desc())
        .limit(limit)
        .all()
    )

    return [
        {
            "id": emp.id,
            "name": emp.name,
            "email": emp.email,
            "department": emp.department,
            "risk_score": emp.risk_score,
            "risk_level": emp.risk_level
        }
        for emp in employees
    ]

@router.get("/risk/dashboard")
def risk_dashboard(
    db: Session = Depends(get_db)
):

    total = db.query(Employee).count()

    low = db.query(Employee).filter(
        Employee.risk_level == "Low"
    ).count()

    medium = db.query(Employee).filter(
        Employee.risk_level == "Medium"
    ).count()

    high = db.query(Employee).filter(
        Employee.risk_level == "High"
    ).count()

    critical = db.query(Employee).filter(
        Employee.risk_level == "Critical"
    ).count()

    average_score = db.query(
        func.avg(Employee.risk_score)
    ).scalar()

    return {
        "total_employees": total,
        "low_risk": low,
        "medium_risk": medium,
        "high_risk": high,
        "critical_risk": critical,
        "average_risk_score": round(average_score or 0, 2)
    }