from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import func, distinct

from app.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_query(self, db: Session):
        return db.query(self.model)

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def get_date_parts(
            self, db: Session, *, column: str, part: str
    ) -> Union[List[int], None]:
        """
        GET DATE PARTS
        :param db: SQLAlchemy Session
        :param column: String representing a Model-column (e.g. "created_at"
        :param part: String representing the date parts: "YEAR" / "MONTH" / "DAY"
        :return: A sorted list of integers
        """
        column_attr = getattr(self.model, column, None)
        if not column_attr:
            return None
        parts = db.query(distinct(func.date_part(part, column_attr)))
        if not parts:
            return None
        parts_sorted_list = sorted([int(part[0]) for part in parts])
        return parts_sorted_list

    def get_by_kwargs(self, db: Session, **kwargs):
        if not kwargs:
            raise ValueError("no kwargs")
        query = db.query(self.model)
        for key, value in kwargs.items():
            query = query.filter(getattr(self.model, key) == value)
        return query

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj

    def remove_by_kwargs(self, db: Session, **kwargs):
        if not kwargs:
            raise ValueError("no kwargs")
        obj = db.query(self.model)
        for key, value in kwargs.items():
            obj = obj.filter(getattr(self.model, key) == value)
        obj = obj.first()
        db.delete(obj)
        db.commit()
        return obj
