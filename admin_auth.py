from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from database import get_db
from admin_models import Admin
from admin_schemas import (
    AdminRegister,
    AdminLogin,
    ChangePassword
)
from security import (
    hash_password,
    authenticate_password
)
from auth_token import create_access_token
from auth_dependency import get_current_admin
from audit_models import AuditLog


router = APIRouter()



# -----------------------------
# Register Admin
# -----------------------------
@router.post("/admin/register")
def register_admin(
    admin: AdminRegister,
    db: Session = Depends(get_db)
):

    existing = (
        db.query(Admin)
        .filter(Admin.username == admin.username)
        .first()
    )

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


    try:

        db.add(new_admin)
        db.commit()
        db.refresh(new_admin)


        return {
            "message": "Admin registered successfully"
        }


    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )



# -----------------------------
# Login Admin
# -----------------------------
@router.post("/admin/login")
def login_admin(
    admin: AdminLogin,
    db: Session = Depends(get_db)
):

    existing = (
        db.query(Admin)
        .filter(Admin.username == admin.username)
        .first()
    )


    if existing is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid username"
        )


    if not authenticate_password(
        admin.password,
        existing.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )


    token = create_access_token(
        {
            "sub": existing.username
        }
    )


    # Audit Log - Admin Login
    log = AuditLog(
        action="Admin Login",
        performed_by=existing.username,
        module="Authentication",
        details="Administrator logged into the system",
        timestamp=datetime.utcnow()
    )


    db.add(log)
    db.commit()


    return {
        "access_token": token,
        "token_type": "bearer"
    }




# -----------------------------
# Change Password
# -----------------------------
@router.put("/admin/change-password")
def change_password(
    passwords: ChangePassword,
    admin: str = Depends(get_current_admin),
    db: Session = Depends(get_db)
):

    existing_admin = (
        db.query(Admin)
        .filter(Admin.username == admin)
        .first()
    )


    if existing_admin is None:
        raise HTTPException(
            status_code=404,
            detail="Admin not found"
        )


    if not authenticate_password(
        passwords.old_password,
        existing_admin.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Old password is incorrect"
        )


    existing_admin.hashed_password = hash_password(
        passwords.new_password
    )


    db.commit()


    # Audit Log - Password Changed
    log = AuditLog(
        action="Password Changed",
        performed_by=admin,
        module="Authentication",
        details="Administrator changed password",
        timestamp=datetime.utcnow()
    )


    db.add(log)
    db.commit()


    return {
        "message": "Password changed successfully"
    }