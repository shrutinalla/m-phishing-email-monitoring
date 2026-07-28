from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from datetime import datetime
from models import Base


class ClickLog(Base):
    __tablename__ = "click_logs"

    id = Column(Integer, primary_key=True, index=True)

    employee_id = Column(
        Integer,
        ForeignKey("employees.id")
    )

    campaign_id = Column(
        Integer,
        ForeignKey("campaigns.id")
    )

    clicked_time = Column(
        DateTime,
        default=datetime.utcnow
    )

    ip_address = Column(
        String(100),
        nullable=True
    )

    user_agent = Column(
        String(500),
        nullable=True
    )