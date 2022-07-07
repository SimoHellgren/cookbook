from sqlalchemy.orm import Session
from backend.app import models


def get_all(db: Session):
    return db.query(models.Recipe).all()


def get(db: Session, id: int):
    return db.query(models.Recipe).get(id)


def create(db: Session, name: str, servings: float, method: str, tags: str = None):
    db_obj = models.Recipe(name=name, servings=servings, method=method, tags=tags)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete(db: Session, id: int):
    db_obj = db.query(models.Recipe).get(id)
    db.delete(db_obj)
    db.commit()
    return db_obj


def get_ingredients(db: Session, id: int):
    return db.query(models.RecipeIngredient).filter_by(recipe_id=id).all()


def add_ingredient(
    db: Session, recipe_id: int, ingredient_id: int, quantity: float, measure: str
):
    db_obj = models.RecipeIngredient(
        recipe_id=recipe_id,
        ingredient_id=ingredient_id,
        quantity=quantity,
        measure=measure,
    )

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
