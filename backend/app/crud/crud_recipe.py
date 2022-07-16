from typing import List, Optional
from sqlalchemy.orm import Session
from backend.app.models import Recipe, RecipeIngredient
from backend.app.schemas.recipe import RecipeCreate, RecipeUpdate
from backend.app.crud.base import CRUDBase
from backend.app.utils import float_to_decimal


class CRUDRecipe(CRUDBase[Recipe, RecipeCreate, RecipeUpdate]):
    def get_ingredients(self, db: Session, id: int) -> Optional[List[RecipeIngredient]]:
        db_obj = db.query(self.model).get(id)

        return db_obj.ingredients if db_obj else None

    def add_ingredient(
        self,
        db: Session,
        recipe_id: int,
        ingredient_id: int,
        quantity: float,
        measure: str,
        optional: bool,
    ) -> RecipeIngredient:

        db_obj = RecipeIngredient(
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


recipe = CRUDRecipe(Recipe)
