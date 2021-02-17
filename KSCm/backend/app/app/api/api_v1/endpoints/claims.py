from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Claim])
def read_claims(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 999,
    _current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve claims.
    """
    claims = crud.claim.get_multi(db, skip=skip, limit=limit)
    return claims


@router.get("/{id}", response_model=schemas.Store)
def read_claim(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    _current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get claim by ID.
    """
    claim = crud.claim.get(db, id=id)
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")
    return claim
