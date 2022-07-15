from typing import List, Optional
from sqlalchemy.orm import Session
from backend.app import models
from backend.app.utils import float_to_decimal


def get_all(db: Session) -> List[models.Recipe]:
    return db.query(models.Recipe).all()


def get(db: Session, id: int) -> Optional[models.Recipe]:
    return db.query(models.Recipe).get(id)


def create(
    db: Session, name: str, servings: float, method: str, tags: Optional[str] = None
) -> models.Recipe:
    servings_dec = float_to_decimal(servings, 1)
    db_obj = models.Recipe(name=name, servings=servings_dec, method=method, tags=tags)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete(db: Session, id: int) -> Optional[models.Recipe]:
    db_obj = db.query(models.Recipe).get(id)
    db.delete(db_obj)
    db.commit()
    return db_obj


def get_ingredients(db: Session, id: int) -> List[models.RecipeIngredient]:
    return db.query(models.RecipeIngredient).filter_by(recipe_id=id).all()


def add_ingredient(
    db: Session,
    recipe_id: int,
    ingredient_id: int,
    quantity: float,
    measure: str,
    optional: bool,
) -> models.RecipeIngredient:
    db_obj = models.RecipeIngredient(
        recipe_id=recipe_id,
        ingredient_id=ingredient_id,
        quantity=float_to_decimal(quantity, 2),
        measure=measure,
        optional=optional,
    )

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
