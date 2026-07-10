from sqlalchemy import Column,Integer,String,DateTime
from models import Base
from datetime import datetime

class ClickLog(Base):
    __tablename__="click_logs"

    id=Column(Integer,primary_key=True,index=True)
    employee_id=Column(Integer)
    email=Column(String)
    campaign_id=Column(Integer)
    clicked_time=Column(DateTime,default=datetime.utcnow)
    ip_address=Column(String)