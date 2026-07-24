from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from database import get_db
from notification_models import Notification

router = APIRouter(prefix="/notifications", tags=["Notifications"])


# Create Notification
@router.post("/")
def create_notification(
    title: str,
    message: str,
    notification_type: str,
    db: Session = Depends(get_db)
):

    notification = Notification(
        title=title,
        message=message,
        notification_type=notification_type,
        status="Unread",
        created_at=datetime.utcnow()
    )

    db.add(notification)
    db.commit()
    db.refresh(notification)

    return {
        "message": "Notification created",
        "notification": notification
    }


# Get All Notifications
@router.get("/")
def get_notifications(
    db: Session = Depends(get_db)
):

    return (
        db.query(Notification)
        .order_by(Notification.created_at.desc())
        .all()
    )


# Mark Notification as Read
@router.put("/{notification_id}/read")
def mark_as_read(
    notification_id: int,
    db: Session = Depends(get_db)
):

    notification = (
        db.query(Notification)
        .filter(Notification.id == notification_id)
        .first()
    )

    if notification is None:
        raise HTTPException(
            status_code=404,
            detail="Notification not found"
        )

    notification.status = "Read"

    db.commit()

    return {
        "message": "Notification marked as read"
    }


# Delete Notification
@router.delete("/{notification_id}")
def delete_notification(
    notification_id: int,
    db: Session = Depends(get_db)
):

    notification = (
        db.query(Notification)
        .filter(Notification.id == notification_id)
        .first()
    )

    if notification is None:
        raise HTTPException(
            status_code=404,
            detail="Notification not found"
        )

    db.delete(notification)
    db.commit()

    return {
        "message": "Notification deleted"
    }