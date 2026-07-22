from pydantic import BaseModel


class AdminRegister(BaseModel):
    username: str
    email: str
    password: str


class AdminLogin(BaseModel):
    username: str
    password: str