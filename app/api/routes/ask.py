from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.models import Case
from app.db.session import get_db
from app.schemas.ask import AskRequest, AskResponse, EvidenceItem
from app.services.rag_service import (
    build_context,
    build_fallback_answer,
    retrieve_relevant_chunks,
)

router = APIRouter(
    prefix="/cases/{case_id}/ask",
    tags=["ask"],
)


@router.post(
    "",
    response_model=AskResponse,
)
def ask_case_question(
    case_id: UUID,
    payload: AskRequest,
    db: Annotated[Session, Depends(get_db)],
):
    case = db.get(Case, case_id)

    if case is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found",
        )

    retrieved_chunks = retrieve_relevant_chunks(
        db=db,
        case_id=case_id,
        question=payload.question,
        top_k=payload.top_k,
    )

    context = build_context(retrieved_chunks)
    answer = build_fallback_answer(payload.question, retrieved_chunks)

    evidence_used = [
        EvidenceItem(
            chunk_id=item["chunk"].id,
            source_id=item["chunk"].source_id,
            source_title=item["source_title"],
            content=item["chunk"].content,
            similarity_score=item["similarity_score"],
        )
        for item in retrieved_chunks
    ]

    return AskResponse(
        answer=answer,
        evidence_used=evidence_used,
        context=context,
    )