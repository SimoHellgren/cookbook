from decimal import Decimal
from pydantic import BaseModel


class RecipeBase(BaseModel):
    name: str
    servings: Decimal
    method: str
    tags: str


class RecipeCreate(RecipeBase):
    pass


class RecipeUpdate(RecipeBase):
    id: int
