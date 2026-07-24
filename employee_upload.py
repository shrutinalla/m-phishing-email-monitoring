from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Employee
from audit_models import AuditLog
from auth_dependency import get_current_admin
from datetime import datetime
import pandas as pd


router = APIRouter()



@router.post("/employees/upload")
def upload_employees(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    admin: str = Depends(get_current_admin)
):

    df = pd.read_csv(file.file)

    count = 0


    for _, row in df.iterrows():

        employee = Employee(

            name=row["name"],

            email=row["email"],

            department=row["department"]

        )


        db.add(employee)

        count += 1



    db.commit()



    # -----------------------------
    # Audit Log
    # -----------------------------

    log = AuditLog(

        action="Employee Upload",

        performed_by=admin,

        module="Employee",

        details=f"{count} employees uploaded",

        timestamp=datetime.utcnow()

    )


    db.add(log)

    db.commit()



    return {

        "message": "Employees uploaded successfully",

        "employees_added": count

    }