from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from admin_models import Admin
from admin_schemas import AdminRegister
from security import hash_password
from admin_schemas import AdminLogin
from auth_token import create_access_token
from security import authenticate_password

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
    
    print("Password received:", admin.password)
    print("Length:", len(admin.password))

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

@router.post("/admin/login")
def login_admin(
    admin: AdminLogin,
    db: Session = Depends(get_db)
):

    existing = db.query(Admin).filter(
        Admin.username == admin.username
    ).first()

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

    return {
        "access_token": token,
        "token_type": "bearer"
    }