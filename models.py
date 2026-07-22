from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    department = Column(String)
    clicked = Column(Boolean, default=False)
    submitted_credentials = Column(Boolean, default=False)
    risk_score = Column(Integer, default=0)
    risk_level = Column(String, default="Low")