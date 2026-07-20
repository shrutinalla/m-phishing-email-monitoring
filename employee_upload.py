from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Employee
import pandas as pd

router = APIRouter()


@router.post("/employees/upload")
def upload_employees(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
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

    return {

        "message": "Employees uploaded successfully",

        "employees_added": count

    }