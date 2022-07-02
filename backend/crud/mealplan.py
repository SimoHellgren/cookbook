from sqlalchemy.orm import Session
from backend import models


def get_all(db: Session):
    return db.query(models.Mealplan).all()


def get(db: Session, id: int):
    return db.query(models.Mealplan).get(id)


def create(db: Session, date: str, name: str, servings: float):
    db_obj = models.Mealplan(date=date, name=name, servings=servings)

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update(db: Session, id: int, date: str, name: str, servings: float, recipe_id: int):
    db_obj = db.query(models.Mealplan).get(id)

    db_obj.date = date
    db_obj.name = name
    db_obj.servings = servings
    db_obj.recipe_id = recipe_id

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete(db: Session, id: int):
    db_obj = db.query(models.Mealplan).get(id)

    db.delete(db_obj)
    db.commit()
    return db_obj
