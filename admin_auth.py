from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from admin_models import Admin
from admin_schemas import AdminRegister
from security import hash_password

router = APIRouter()


@router.post("/admin/register")
def register_admin(
    admin: AdminRegister,
    db: Session = Depends(get_db)
):

    existing = db.query(Admin).filter(
        Admin.username == admin.username
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    new_admin = Admin(
        username=admin.username,
        email=admin.email,
        hashed_password=hash_password(admin.password)
    )

    db.add(new_admin)
    db.commit()

    return {
        "message": "Admin registered successfully"
    }