from sqlalchemy import Column, Integer, String
from models import Base

class EmailTemplate(Base):
    __tablename__ = "email_templates"

    id = Column(Integer, primary_key=True, index=True)
    template_name = Column(String)
    subject = Column(String)
    content = Column(String)