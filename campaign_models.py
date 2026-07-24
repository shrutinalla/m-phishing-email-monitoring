from sqlalchemy import Column, Integer, String, DateTime
from models import Base
from datetime import datetime
from sqlalchemy import ForeignKey


class Campaign(Base):

    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)

    campaign_name = Column(String, unique=True)

    email_subject = Column(String)

    email_template = Column(String)

    template_id = Column(Integer, ForeignKey("email_templates.id"), nullable=True)

    status = Column(String, default="Draft")

    difficulty = Column(String, default="Easy")

    created_at = Column(DateTime, default=datetime.utcnow)

    start_date = Column(DateTime, nullable=True)

    end_date = Column(DateTime, nullable=True)

    total_recipients = Column(Integer, default=0)

    emails_sent = Column(Integer, default=0)

    emails_failed = Column(Integer, default=0)

    completed_at = Column(DateTime, nullable=True)

    
'''
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime

from models import Base


class Campaign(Base):

    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)

    campaign_name = Column(String, unique=True)

    email_subject = Column(String)

    email_template = Column(String)

    template_id = Column(
        Integer,
        ForeignKey("email_templates.id"),
        nullable=True
    )

    status = Column(String, default="Draft")

    difficulty = Column(String, default="Easy")

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    start_date = Column(
        DateTime,
        nullable=True
    )

    end_date = Column(
        DateTime,
        nullable=True
    )'''