from sqlalchemy import Column, Integer, String, DateTime, Boolean
from models import Base
from datetime import datetime


class Notification(Base):

    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String)

    message = Column(String)

    notification_type = Column(String)

    status = Column(String, default="Unread")

    is_read = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)