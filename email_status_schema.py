from pydantic import BaseModel


class EmailStatusResponse(BaseModel):
    employee_email: str
    campaign_name: str
    status: str