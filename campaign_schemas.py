from pydantic import BaseModel

class CampaignCreate(BaseModel):
    campaign_name: str
    email_subject: str
    email_template: str