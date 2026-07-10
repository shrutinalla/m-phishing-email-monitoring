from pydantic import BaseModel

class TemplateCreate(BaseModel):
    template_name: str
    subject: str
    content: str

