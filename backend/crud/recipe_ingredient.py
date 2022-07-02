from sqlalchemy.orm import Session
from backend import models


def get_all(db: Session):
    return db.query(models.RecipeIngredient).all()
