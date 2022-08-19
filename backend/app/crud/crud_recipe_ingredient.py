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

    def update_many(
        self, db: Session, data: list[tuple[RecursionError, RecipeIngredientUpdate]]
    ) -> list[RecipeIngredient]:
        # set positions temporarily to large values to avoid uniqueness conflicts
        for db_obj, _ in data:
            setattr(db_obj, "position", db_obj.position + 10000)
            db.add(db_obj)

        db.commit()

        # then do the actual updates
        for db_obj, obj_in in data:
            for field, value in obj_in.dict().items():
                setattr(db_obj, field, value)

        for obj, _ in data:
            db.add(obj)

        db.commit()

        for obj, _ in data:
            db.refresh(obj)

        return [obj for obj, _ in data]

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
