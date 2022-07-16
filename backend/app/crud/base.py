from typing import Generic, List, Optional, Type, TypeVar
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.app.db.base_class import Base


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, id: int) -> Optional[ModelType]:
        return db.query(self.model).get(id)

    def get_many(self, db: Session) -> List[ModelType]:
        return db.query(self.model).all()

    def create(self, db: Session, obj_in: CreateSchemaType) -> ModelType:
        db_obj = self.model(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, db_obj: ModelType, obj_in: UpdateSchemaType
    ) -> ModelType:
        for field, value in obj_in.dict().items():
            setattr(db_obj, field, value)

        db.add(db_obj)
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, id: int) -> Optional[ModelType]:
        db_obj = db.query(self.model).get(id)
        db.delete(db_obj)
        db.commit()
        return db_obj
