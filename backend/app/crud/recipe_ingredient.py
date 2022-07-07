from sqlalchemy.orm import Session
from backend.app import models


def get_all(db: Session):
    return db.query(models.RecipeIngredient).all()
