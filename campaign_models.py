from sqlalchemy import Column, Integer, String, DateTime
from models import Base
from datetime import datetime


class Campaign(Base):

    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)

    campaign_name = Column(String, unique=True)

    email_subject = Column(String)

    email_template = Column(String)

    status = Column(String, default="Draft")

    difficulty = Column(String, default="Easy")

    created_at = Column(DateTime, default=datetime.utcnow)

    start_date = Column(DateTime, nullable=True)

    end_date = Column(DateTime, nullable=True)