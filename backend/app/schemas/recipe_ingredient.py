from decimal import Decimal
from pydantic import BaseModel


class RecipeIngredientBase(BaseModel):
    recipe_id: int
    ingredient_id: int
    quantity: Decimal
    measure: str
    optional: bool


class RecipeIngredientCreate(RecipeIngredientBase):
    pass


class RecipeIngredientUpdate(RecipeIngredientBase):
    pass
