from pydantic import BaseModel


class AuditLogCreate(BaseModel):
    action: str
    performed_by: str
    module: str
    details: str