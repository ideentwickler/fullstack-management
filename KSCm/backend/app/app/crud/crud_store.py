from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.store import Store, StoreSupport
from app.schemas.store import StoreCreate, StoreUpdate


class CRUDStore(CRUDBase[Store, StoreCreate, StoreUpdate]):
    def create(self, db: Session, *, obj_in: StoreCreate) -> Store:
        obj_in.name = obj_in.name.upper()
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


store = CRUDStore(Store)
