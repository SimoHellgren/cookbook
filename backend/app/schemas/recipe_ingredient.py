from decimal import Decimal
from pydantic import BaseModel
from backend.app.schemas.ingredient import Ingredient


class RecipeIngredientBase(BaseModel):
    recipe_id: int
    ingredient_id: int
    quantity: Decimal
    measure: str
    optional: bool
    position: int


class RecipeIngredientCreate(RecipeIngredientBase):
    pass


class RecipeIngredientUpdate(RecipeIngredientBase):
    pass


class RecipeIngredient(RecipeIngredientBase):
    """For use as API response model"""

    ingredient: Ingredient

    class Config:
        orm_mode = True
