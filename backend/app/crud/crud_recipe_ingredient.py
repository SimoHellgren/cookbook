from typing import Optional
from sqlalchemy.orm import Session
from backend.app.crud.base import CRUDBase
from backend.app.models.recipe_ingredient import RecipeIngredient
from backend.app.schemas.recipe_ingredient import (
    RecipeIngredientCreate,
    RecipeIngredientUpdate,
)


class CRUDRecipeIngredient(
    CRUDBase[RecipeIngredient, RecipeIngredientCreate, RecipeIngredientUpdate]
):
    def get(
        self, db: Session, recipe_id: int, ingredient_id: int
    ) -> Optional[RecipeIngredient]:
        return (
            db.query(RecipeIngredient)
            .filter_by(recipe_id=recipe_id, ingredient_id=ingredient_id)
            .first()
        )

    def remove(
        self, db: Session, recipe_id: int, ingredient_id: int
    ) -> Optional[RecipeIngredient]:
        db_obj = (
            db.query(RecipeIngredient)
            .filter_by(recipe_id=recipe_id, ingredient_id=ingredient_id)
            .first()
        )
        db.delete(db_obj)
        db.commit()
        return db_obj


recipe_ingredient = CRUDRecipeIngredient(RecipeIngredient)
