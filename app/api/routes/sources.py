from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Case, Source, Chunk
from app.db.session import get_db
from app.schemas.source import SourceCreate, SourceResponse
from app.services.chunking_service import chunk_text
from app.services.embedding_service import generate_embeddings

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
    
    chunks = chunk_text(payload.content)

    if not chunks:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Source content must not be empty",
        )
    
    embeddings = generate_embeddings(chunks)

    source = Source(
        case_id=case_id,
        title=payload.title,
        content=payload.content,
    )

    db.add(source)
    db.flush()

    chunk_records = [
        Chunk(
            source_id=source.id,
            content=chunk,
            embedding=embedding,
        )
        for chunk, embedding in zip(chunks, embeddings)
    ]

    db.add_all(chunk_records)
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

@router.get(
    "/{source_id}/chunks",
)
def list_source_chunks(
    case_id: UUID,
    source_id: UUID,
    db: Annotated[Session, Depends(get_db)],
):
    source = db.get(Source, source_id)

    if source is None or source.case_id != case_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Source not found",
        )

    statement = (
        select(Chunk)
        .where(Chunk.source_id == source_id)
        .order_by(Chunk.created_at.asc())
    )

    chunks = db.scalars(statement).all()

    return [
        {
            "id": chunk.id,
            "source_id": chunk.source_id,
            "content": chunk.content,
            "embedding_dimensions": len(chunk.embedding),
            "created_at": chunk.created_at,
        }
        for chunk in chunks
    ]