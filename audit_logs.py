from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from zoneinfo import ZoneInfo
from database import get_db
from audit_models import AuditLog
from audit_schemas import AuditLogCreate

router = APIRouter(
    prefix="/audit-logs",
    tags=["Audit Logs"]
)


# Create Audit Log
@router.post("/")
def create_audit_log(
    log: AuditLogCreate,
    db: Session = Depends(get_db)
):

    new_log = AuditLog(
        action=log.action,
        performed_by=log.performed_by,
        module=log.module,
        details=log.details,
        timestamp=datetime.now(ZoneInfo("Asia/Kolkata"))
    )

    db.add(new_log)
    db.commit()
    db.refresh(new_log)

    return {
        "message": "Audit log created successfully",
        "audit_log": new_log
    }


# Get All Logs
@router.get("/")
def get_all_logs(
    db: Session = Depends(get_db)
):

    return (
        db.query(AuditLog)
        .order_by(AuditLog.timestamp.desc())
        .all()
    )


# Get One Log
@router.get("/{log_id}")
def get_log(
    log_id: int,
    db: Session = Depends(get_db)
):

    log = (
        db.query(AuditLog)
        .filter(AuditLog.id == log_id)
        .first()
    )

    if log is None:
        raise HTTPException(
            status_code=404,
            detail="Audit log not found"
        )

    return log


# Delete Log
@router.delete("/{log_id}")
def delete_log(
    log_id: int,
    db: Session = Depends(get_db)
):

    log = (
        db.query(AuditLog)
        .filter(AuditLog.id == log_id)
        .first()
    )

    if log is None:
        raise HTTPException(
            status_code=404,
            detail="Audit log not found"
        )

    db.delete(log)
    db.commit()

    return {
        "message": "Audit log deleted successfully"
    }