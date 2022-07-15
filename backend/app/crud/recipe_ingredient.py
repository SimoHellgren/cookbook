from typing import List
from sqlalchemy.orm import Session
from backend.app import models


def get_all(db: Session) -> List[models.RecipeIngredient]:
    return db.query(models.RecipeIngredient).all()
