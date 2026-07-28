from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CampaignCreate(BaseModel):

    campaign_name: str
    email_subject: str
    email_template: str

    difficulty: Optional[str] = "Easy"
    status: Optional[str] = "Draft"
    template_id: Optional[int] = None


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

    template_id: Optional[int]

    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

    total_recipients: int
    emails_sent: int
    emails_failed: int

    completed_at: Optional[datetime] = None

    # -------------------------
    # Attachment Metadata
    # -------------------------

    attachment_name: Optional[str] = None
    attachment_type: Optional[str] = None
    attachment_size: Optional[int] = None

    class Config:
        from_attributes = True