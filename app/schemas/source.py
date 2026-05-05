from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class SourceCreate(BaseModel):
    title: str
    content: str


class SourceResponse(BaseModel):
    id: UUID
    case_id: UUID
    title: str
    content: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)