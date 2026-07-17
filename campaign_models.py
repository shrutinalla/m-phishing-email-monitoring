from sqlalchemy import Column, Integer, String
from models import Base

class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    campaign_name = Column(String)
    email_subject = Column(String)
    email_template = Column(String)
difficulty = Column(String, default="Easy") 