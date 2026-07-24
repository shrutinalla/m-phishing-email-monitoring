from sqlalchemy import Column, Integer, String, DateTime
from models import Base
from datetime import datetime


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)

    action = Column(String)

    performed_by = Column(String)

    module = Column(String)

    details = Column(String)

    timestamp = Column(DateTime, default=datetime.utcnow)