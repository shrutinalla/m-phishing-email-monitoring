from sqlalchemy import Column, Integer, String, DateTime
from models import Base
from datetime import datetime


class EmailLog(Base):

    __tablename__ = "email_logs"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    employee_id = Column(
        Integer
    )


    campaign_id = Column(
        Integer
    )


    email = Column(
        String
    )


    status = Column(
        String,
        default="Pending"
    )


    sent_time = Column(
        DateTime,
        default=datetime.utcnow
    )


    error_message = Column(
        String,
        nullable=True
    )