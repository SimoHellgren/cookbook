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
            .filter(recipe_id=recipe_id, ingredient_id=ingredient_id)
            .first()
        )


recipe_ingredient = CRUDRecipeIngredient(RecipeIngredient)
