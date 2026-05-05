from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CaseCreate(BaseModel):
    title: str
    company_name: str | None = None


class CaseResponse(BaseModel):
    id: UUID
    title: str
    company_name: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)