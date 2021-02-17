from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Store])
def read_stores(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 999,
    _current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve stores.
    """
    stores = crud.store.get_multi(db, skip=skip, limit=limit)
    return stores


@router.post("/", response_model=schemas.Store)
def create_store(
    *,
    db: Session = Depends(deps.get_db),
    store_in: schemas.StoreCreate,
    _current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new store.
    """
    store = crud.store.create(db, obj_in=store_in)
    return store


@router.put("/{internal_id}", response_model=schemas.Store)
def update_store(
    *,
    db: Session = Depends(deps.get_db),
    internal_id: int,
    store_in: schemas.StoreUpdate,
    _current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an item.
    """
    store = crud.store.get_by_kwargs(db, internal_id=internal_id).first()
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    store = crud.store.update(db, db_obj=store, obj_in=store_in)
    return store


@router.get("/{internal_id}", response_model=schemas.Store)
def read_store(
    *,
    db: Session = Depends(deps.get_db),
    internal_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get item by ID.
    """
    store = crud.store.get_by_kwargs(db, internal_id=internal_id).first()
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    return store


@router.delete("/{internal_id}", response_model=schemas.Item)
def delete_store(
    *,
    db: Session = Depends(deps.get_db),
    internal_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an item.
    """
    store = crud.store.get_by_kwargs(db, internal_id=internal_id).first()
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    store = crud.item.remove_by_kwargs(db, internal_id=internal_id)
    return store
