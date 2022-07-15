from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from backend.app import models
from backend.app.utils import float_to_decimal


def get_all(db: Session) -> List[models.Mealplan]:
    return db.query(models.Mealplan).all()


def get(db: Session, id: int) -> Optional[models.Mealplan]:
    return db.query(models.Mealplan).get(id)


def create(
    db: Session, date: str, name: str, servings: float
) -> Optional[models.Mealplan]:

    db_obj = models.Mealplan(
        date=datetime.strptime(date, "%Y-%m-%d").date(),
        name=name,
        servings=float_to_decimal(servings, 1),
    )

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update(
    db: Session, id: int, date: str, name: str, servings: float, recipe_id: int
) -> Optional[models.Mealplan]:
    db_obj = db.query(models.Mealplan).get(id)

    if not db_obj:
        return None

    db_obj.date = datetime.strptime(date, "%Y-%m-%d").date()
    db_obj.name = name
    db_obj.servings = float_to_decimal(servings, 1)
    db_obj.recipe_id = recipe_id

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete(db: Session, id: int) -> Optional[models.Mealplan]:
    db_obj = db.query(models.Mealplan).get(id)

    db.delete(db_obj)
    db.commit()
    return db_obj
