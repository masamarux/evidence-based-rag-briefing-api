from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Case
from app.db.session import get_db
from app.schemas.case import CaseCreate, CaseResponse

router = APIRouter(
    prefix="/cases",
    tags=["cases"],
)


@router.post(
    "",
    response_model=CaseResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_case(
    payload: CaseCreate,
    db: Annotated[Session, Depends(get_db)],
):
    case = Case(
        title=payload.title,
        company_name=payload.company_name,
    )

    db.add(case)
    db.commit()
    db.refresh(case)

    return case


@router.get(
    "",
    response_model=list[CaseResponse],
)
def list_cases(
    db: Annotated[Session, Depends(get_db)],
):
    statement = select(Case).order_by(Case.created_at.desc())
    cases = db.scalars(statement).all()

    return cases


@router.get(
    "/{case_id}",
    response_model=CaseResponse,
)
def get_case(
    case_id: UUID,
    db: Annotated[Session, Depends(get_db)],
):
    case = db.get(Case, case_id)

    if case is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found",
        )

    return case