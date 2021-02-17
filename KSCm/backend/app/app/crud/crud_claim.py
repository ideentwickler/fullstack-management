from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.claim import Claim
from app.schemas.claim import ClaimCreate, ClaimUpdate


class CRUDClaim(CRUDBase[Claim, ClaimCreate, ClaimUpdate]):
    def create(self, db: Session, *, obj_in: ClaimCreate) -> Claim:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


claim = CRUDClaim(Claim)
