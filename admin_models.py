from sqlalchemy import Column, Integer, String
from models import Base


class Admin(Base):

    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String, unique=True, nullable=False)

    email = Column(String, unique=True, nullable=False)

    hashed_password = Column(String, nullable=False)
    