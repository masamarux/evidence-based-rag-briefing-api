from uuid import UUID

from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    question: str = Field(min_length=1)
    top_k: int = Field(default=5, ge=1, le=10)


class EvidenceItem(BaseModel):
    chunk_id: UUID
    source_id: UUID
    source_title: str
    content: str
    similarity_score: float


class AskResponse(BaseModel):
    answer: str
    evidence_used: list[EvidenceItem]
    context: str