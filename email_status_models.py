from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from models import Base


class EmailStatus(Base):
    __tablename__ = "email_status"

    id = Column(Integer, primary_key=True, index=True)

    employee_email = Column(String, nullable=False)

    campaign_name = Column(String, nullable=False)

    status = Column(String, default="Pending")

    sent_at = Column(DateTime, default=datetime.utcnow)