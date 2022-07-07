from typing import List
from sqlalchemy.orm import Session
from backend.app import models


def get_all(db: Session) -> List[models.Ingredient]:
    return db.query(models.Ingredient).all()


def create(db: Session, name: str) -> models.Ingredient:
    # try to return existing value
    db_obj = db.query(models.Ingredient).filter_by(name=name).first()
    if db_obj:
        return db_obj

    db_obj = models.Ingredient(name=name)

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
