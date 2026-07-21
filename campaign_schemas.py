from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CampaignCreate(BaseModel):

    campaign_name: str

    email_subject: str

    email_template: str

    difficulty: Optional[str] = "Easy"
    status: Optional[str] = "Draft"


class CampaignUpdate(BaseModel):

    campaign_name: str

    email_subject: str

    email_template: str

    difficulty: str

    status: str

class CampaignStatusUpdate(BaseModel):
    status: str


class CampaignSchedule(BaseModel):
    start_date: datetime
    end_date: datetime

class CampaignResponse(BaseModel):

    id: int

    campaign_name: str

    email_subject: str

    email_template: str

    difficulty: str

    status: str

    created_at: datetime

    class Config:
        from_attributes = True