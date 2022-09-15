from decimal import Decimal
from typing import Optional
from sqlalchemy.orm import Session
from backend.app.models import Recipe, RecipeIngredient
from backend.app.models.comment import Comment
from backend.app.schemas.recipe import RecipeCreate, RecipeUpdate
from backend.app.crud.base import CRUDBase


class CRUDRecipe(CRUDBase[Recipe, RecipeCreate, RecipeUpdate]):
    def get_ingredients(self, db: Session, id: int) -> Optional[list[RecipeIngredient]]:
        db_obj = db.query(self.model).get(id)

        return db_obj.ingredients if db_obj else None

    def add_ingredient(
        self,
        db: Session,
        recipe_id: int,
        ingredient_id: int,
        quantity: Decimal,
        measure: str,
        optional: bool,
        position: int,
    ) -> RecipeIngredient:

        db_obj = RecipeIngredient(
            recipe_id=recipe_id,
            ingredient_id=ingredient_id,
            quantity=quantity,
            measure=measure,
            optional=optional,
            position=position,
        )

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_comments(self, db: Session, id: int) -> Optional[list[Comment]]:
        db_obj = db.query(self.model).get(id)

        return db_obj.comments if db_obj else None


recipe = CRUDRecipe(Recipe)
