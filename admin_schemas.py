from pydantic import BaseModel, EmailStr


class AdminRegister(BaseModel):
    username: str
    email: EmailStr
    password: str


class AdminLogin(BaseModel):
    username: str
    password: str

class ChangePassword(BaseModel):
    old_password: str
    new_password: str