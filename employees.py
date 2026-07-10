from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Employee
from pydantic import BaseModel

router=APIRouter()

class EmployeeCreate(BaseModel):
    name:str
    email:str
    department:str


@router.post("/employees")
def create_employee(
employee:EmployeeCreate,
db:Session=Depends(get_db)
):

    emp=Employee(
        name=employee.name,
        email=employee.email,
        department=employee.department
    )

    db.add(emp)
    db.commit()

    return {"message":"Employee added"}