from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Case, Source
from app.db.session import get_db
from app.schemas.source import SourceCreate, SourceResponse

router = APIRouter(
    prefix="/cases/{case_id}/sources",
    tags=["sources"],
)


@router.post(
    "",
    response_model=SourceResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_source(
    case_id: UUID,
    payload: SourceCreate,
    db: Annotated[Session, Depends(get_db)],
):
    case = db.get(Case, case_id)

    if case is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found",
        )

    source = Source(
        case_id=case_id,
        title=payload.title,
        content=payload.content,
    )

    db.add(source)
    db.commit()
    db.refresh(source)

    return source


@router.get(
    "",
    response_model=list[SourceResponse],
)
def list_sources(
    case_id: UUID,
    db: Annotated[Session, Depends(get_db)],
):
    case = db.get(Case, case_id)

    if case is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found",
        )

    statement = (
        select(Source)
        .where(Source.case_id == case_id)
        .order_by(Source.created_at.desc())
    )

    sources = db.scalars(statement).all()

    return sources